// Native tests for the SS09a modeswitch state machine. Run: g++ -std=c++17 test_native.cpp && ./a.out
#include "state_machine.h"
#include <cassert>
#include <cstdio>
using namespace modeswitch;

static int passed = 0;
#define CHECK(x) do { if (!(x)) { printf("FAIL line %d: %s\n", __LINE__, #x); return 1; } passed++; } while (0)

// helper: run machine to steady STORE from cold start
static Inputs base(uint32_t t) { Inputs i; i.now_ms = t; return i; }

int main() {
  { // happy path: IDLE -> STORE
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::STORE; in.hv_bus_v = 0;
    m.tick(in);                              // begin: QUIESCE
    CHECK(m.state().phase == Phase::QUIESCE);
    in.now_ms = 100; m.tick(in);             // quiet -> VERIFY_SAFE (then flip prep)
    in.now_ms = 200; m.tick(in);             // hv safe -> SWITCHING, all dead
    CHECK(m.state().phase == Phase::SWITCHING);
    CHECK(!m.state().mux_engage && !m.state().car_lv_power);
    in.now_ms = 900; m.tick(in);             // dwell passed -> engage branch B
    CHECK(m.state().phase == Phase::WAKE);
    CHECK(m.state().mux_engage && !m.state().mux_select_car && !m.state().car_lv_power);
    in.be_heartbeat = true; in.now_ms = 1000; m.tick(in);
    CHECK(m.state().phase == Phase::STEADY && m.state().active == Mode::STORE);
  }
  { // STORE -> CAMP: car branch + LV gate on, waits for car boot
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::STORE;
    m.tick(in); in.now_ms=1; m.tick(in); in.now_ms=2; m.tick(in);
    in.now_ms=600; m.tick(in); in.be_heartbeat = true; in.now_ms=700; m.tick(in);
    CHECK(m.state().active == Mode::STORE);
    in.selector = Mode::CAMP; in.be_heartbeat = false; in.now_ms = 1000; m.tick(in);
    CHECK(m.state().phase == Phase::QUIESCE);
    CHECK(m.state().request_be_open_contactors);   // BE asked to open contactors
    in.now_ms = 1100; m.tick(in); in.now_ms = 1200; m.tick(in);
    in.now_ms = 1800; m.tick(in);                  // dwell done -> branch A + LV on
    CHECK(m.state().phase == Phase::WAKE);
    CHECK(m.state().mux_select_car && m.state().car_lv_power);
    in.car_awake = true; in.now_ms = 40000; m.tick(in); // car booted
    CHECK(m.state().active == Mode::CAMP);
  }
  { // refusal: DRIVE without 7-pin
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::DRIVE; in.seven_pin_present = false;
    m.tick(in);
    CHECK(m.state().phase == Phase::STEADY && m.state().active == Mode::IDLE);
    CHECK(m.state().last_refusal == Refusal::NO_SEVEN_PIN);
    in.seven_pin_present = true; in.now_ms = 100; m.tick(in);   // now allowed
    CHECK(m.state().phase == Phase::QUIESCE);
  }
  { // refusal: cannot leave DRIVE while moving; allowed once stopped
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::DRIVE; in.seven_pin_present = true;
    m.tick(in); in.now_ms=1; m.tick(in); in.now_ms=2; m.tick(in);
    in.now_ms=600; m.tick(in); in.be_heartbeat = true; in.now_ms=700; m.tick(in);
    CHECK(m.state().active == Mode::DRIVE);
    in.selector = Mode::CAMP; in.motion = true; in.now_ms = 1000; m.tick(in);
    CHECK(m.state().active == Mode::DRIVE && m.state().last_refusal == Refusal::IN_MOTION);
    in.motion = false; in.now_ms = 1100; m.tick(in);
    CHECK(m.state().phase == Phase::QUIESCE);
  }
  { // refusal: mid-charge
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::STORE;
    m.tick(in); in.now_ms=1; m.tick(in); in.now_ms=2; m.tick(in);
    in.now_ms=600; m.tick(in); in.be_heartbeat = true; in.now_ms=700; m.tick(in);
    in.selector = Mode::CAMP; in.pack_current_valid = true; in.pack_current_a = 20.0f;
    in.now_ms = 1000; m.tick(in);
    CHECK(m.state().active == Mode::STORE && m.state().last_refusal == Refusal::CHARGING);
  }
  { // fault: HV never decays -> latched safe idle, alarm; reset clears
    Config c; c.verify_ms = 1000;
    StateMachine m(c);
    Inputs in = base(0); in.selector = Mode::STORE; in.hv_bus_v = 350;
    m.tick(in); in.now_ms = 10; m.tick(in);          // QUIESCE -> VERIFY (quiet immediately)
    CHECK(m.state().phase == Phase::VERIFY_SAFE);
    in.now_ms = 2000; m.tick(in);                    // verify timeout
    CHECK(m.state().phase == Phase::FAULTED && m.state().alarm);
    CHECK(!m.state().mux_engage && !m.state().car_lv_power);
    in.fault_reset = true; in.now_ms = 3000; m.tick(in);
    CHECK(m.state().phase == Phase::STEADY && m.state().active == Mode::IDLE && !m.state().alarm);
  }
  { // estop: instant nobody-is-master from any state
    StateMachine m;
    Inputs in = base(0); in.selector = Mode::STORE;
    m.tick(in); in.now_ms=1; m.tick(in); in.now_ms=2; m.tick(in);
    in.now_ms=600; m.tick(in); in.be_heartbeat = true; in.now_ms=700; m.tick(in);
    in.estop = true; in.now_ms = 800; m.tick(in);
    CHECK(m.state().phase == Phase::FAULTED && !m.state().mux_engage);
  }
  printf("ALL PASS (%d checks)\n", passed);
  return 0;
}
