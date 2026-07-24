// modeswitch — SS09a pack-master mode handoff supervisor (state machine core)
// Pure logic: no Arduino/ESP32 dependencies. Compiled identically on the ESP32
// and natively for tests. The invention is this sequence — trust it, not the silicon.
// License: MIT (Slipstream project, github.com/divergent-futures/slipstream)
#pragma once
#include <cstdint>
#include <cmath>

namespace modeswitch {

// Operator-selectable modes (3-position keyed selector). IDLE = no master (safe).
enum class Mode : uint8_t { IDLE, CAMP, DRIVE, STORE };
// Handoff phases. Every transition walks QUIESCE -> VERIFY_SAFE -> SWITCHING -> WAKE.
enum class Phase : uint8_t { STEADY, QUIESCE, VERIFY_SAFE, SWITCHING, WAKE, FAULTED };
enum class Refusal : uint8_t { NONE, NO_SEVEN_PIN, IN_MOTION, CHARGING, ESTOP };

struct Config {
  float hv_safe_v        = 50.0f;   // HV bus must decay below this before any flip
  float i_safe_a         = 2.0f;    // and pack current below this
  float i_charge_a       = 5.0f;    // above this at request time = refuse (mid-charge)
  uint32_t quiesce_ms    = 120000;  // car shutdown can be slow
  uint32_t verify_ms     = 60000;
  uint32_t switch_dwell_ms = 500;   // both-branches-dead dwell (break-before-make)
  uint32_t wake_ms       = 90000;   // car boot ~30-60 s
};

struct Inputs {
  uint32_t now_ms = 0;
  Mode selector = Mode::IDLE;       // operator request
  float hv_bus_v = 0;               // isolated divider
  float pack_current_a = 0;         // from BE broadcast when on bus
  bool  pack_current_valid = false;
  bool  seven_pin_present = false;  // tow vehicle connected (DRIVE permissive)
  bool  motion = false;             // wheel speed > 0
  bool  car_awake = false;          // CAN-A activity heard
  bool  be_heartbeat = false;       // CAN-B Battery-Emulator alive
  bool  estop = false;
  bool  fault_reset = false;        // momentary button
};

struct Outputs {
  bool mux_engage = false;          // relay 1: pack CAN connected to anything at all
  bool mux_select_car = false;      // relay 2: branch A (car) vs B (open stack)
  bool car_lv_power = false;        // gate for the ENTIRE car-ECU set
  bool request_be_open_contactors = false; // CAN message shim (main.cpp sends it)
  bool alarm = false;
  Mode active = Mode::IDLE;
  Mode target = Mode::IDLE;
  Phase phase = Phase::STEADY;
  Refusal last_refusal = Refusal::NONE;
};

class StateMachine {
public:
  explicit StateMachine(const Config& c = Config{}) : cfg(c) {}

  const Outputs& tick(const Inputs& in) {
    if (in.estop) { fault(); out.last_refusal = Refusal::ESTOP; return out; }
    switch (out.phase) {
      case Phase::FAULTED:
        if (in.fault_reset) { // operator acknowledges -> safe idle, alarm off
          out = Outputs{}; out.active = Mode::IDLE; out.phase = Phase::STEADY;
        }
        break;
      case Phase::STEADY:
        if (in.selector != out.active) beginTransition(in);
        break;
      case Phase::QUIESCE: {
        // leaving CAMP: wait for the car to finish sleeping; leaving DRIVE/STORE:
        // BE is asked to open contactors and go quiet. IDLE has nothing to quiesce.
        bool quiet = (out.active == Mode::CAMP) ? !in.car_awake : true; // BE obeys; VERIFY confirms
        if (quiet) enter(Phase::VERIFY_SAFE, in.now_ms);
        else if (elapsed(in) > cfg.quiesce_ms) fault();
        break;
      }
      case Phase::VERIFY_SAFE: {
        bool currentOk = !in.pack_current_valid || std::fabs(in.pack_current_a) < cfg.i_safe_a;
        if (in.hv_bus_v < cfg.hv_safe_v && currentOk) {
          // the flip: everything dead first
          out.mux_engage = false;
          out.car_lv_power = false;
          out.request_be_open_contactors = false;
          enter(Phase::SWITCHING, in.now_ms);
        } else if (elapsed(in) > cfg.verify_ms) fault();
        break;
      }
      case Phase::SWITCHING:
        if (elapsed(in) >= cfg.switch_dwell_ms) { // both branches provably dead for the dwell
          if (out.target == Mode::IDLE) { steady(Mode::IDLE); break; }
          out.mux_select_car = (out.target == Mode::CAMP);
          out.mux_engage = true;
          out.car_lv_power = (out.target == Mode::CAMP);
          enter(Phase::WAKE, in.now_ms);
        }
        break;
      case Phase::WAKE: {
        bool alive = (out.target == Mode::CAMP) ? in.car_awake : in.be_heartbeat;
        if (alive) steady(out.target);
        else if (elapsed(in) > cfg.wake_ms) fault();
        break;
      }
    }
    return out;
  }

  const Outputs& state() const { return out; }

private:
  void beginTransition(const Inputs& in) {
    out.last_refusal = Refusal::NONE;
    // refusal rules — the supervisor says no and stays put
    if (out.active == Mode::DRIVE && in.motion)            { refuse(Refusal::IN_MOTION); return; }
    if (in.selector == Mode::DRIVE && !in.seven_pin_present){ refuse(Refusal::NO_SEVEN_PIN); return; }
    if (in.selector == Mode::CAMP && in.motion)            { refuse(Refusal::IN_MOTION); return; }
    if (in.pack_current_valid && std::fabs(in.pack_current_a) > cfg.i_charge_a)
                                                           { refuse(Refusal::CHARGING); return; }
    out.target = in.selector;
    out.request_be_open_contactors = (out.active == Mode::DRIVE || out.active == Mode::STORE);
    enter(Phase::QUIESCE, in.now_ms);
  }
  void refuse(Refusal r) { out.last_refusal = r; }
  void enter(Phase p, uint32_t now) { out.phase = p; phase_t0 = now; }
  void steady(Mode m) { out.active = m; out.target = m; out.phase = Phase::STEADY; out.alarm = false; }
  void fault() { // worst failure = nobody is master = safe idle, latched, loud
    out.mux_engage = false; out.mux_select_car = false; out.car_lv_power = false;
    out.request_be_open_contactors = false; out.alarm = true; out.phase = Phase::FAULTED;
    out.active = Mode::IDLE;
  }
  uint32_t elapsed(const Inputs& in) const { return in.now_ms - phase_t0; }
  Config cfg; Outputs out{}; uint32_t phase_t0 = 0;
};

} // namespace modeswitch
