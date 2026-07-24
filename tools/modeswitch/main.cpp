// modeswitch — ESP32 hardware shell for the SS09a supervisor.
// The brains live in state_machine.h (tested natively — run test_native.cpp).
// This file is ONLY shims: pins, debounce, CAN, and the 1 Hz status broadcast.
// Board: any ESP32 devkit + 2x automotive relay driver + isolated HV divider.
// TODO(bench): every constant marked BENCH is characterized on the Phase-A bench.
#include "state_machine.h"
#include <Arduino.h>
// #include <driver/twai.h>   // ESP32 built-in CAN (TWAI) — enable at bench bring-up

using namespace modeswitch;

// ---- pin map (draft — final at enclosure build) ----
constexpr int PIN_SEL_CAMP   = 32;  // 3-position keyed selector (one input per position,
constexpr int PIN_SEL_DRIVE  = 33;  //  all open = IDLE request)
constexpr int PIN_SEL_STORE  = 25;
constexpr int PIN_RELAY_ENGAGE = 26; // relay 1: pack CAN connected at all
constexpr int PIN_RELAY_SELECT = 27; // relay 2: branch A (car) / B (open stack)
constexpr int PIN_CAR_LV_GATE  = 14; // gate for the ENTIRE car-ECU set
constexpr int PIN_HV_SENSE     = 34; // isolated divider, ADC   BENCH: calibrate scale
constexpr int PIN_7PIN_SENSE   = 35; // tow-vehicle presence (same permissive as followdrive)
constexpr int PIN_ESTOP        = 4;  // NC loop, opens = estop
constexpr int PIN_FAULT_RESET  = 5;  // momentary
constexpr int PIN_ALARM        = 13; // buzzer + LED

StateMachine sm;   // default Config{} — thresholds documented in state_machine.h

static Mode readSelector() {
  if (!digitalRead(PIN_SEL_CAMP))  return Mode::CAMP;   // active-low
  if (!digitalRead(PIN_SEL_DRIVE)) return Mode::DRIVE;
  if (!digitalRead(PIN_SEL_STORE)) return Mode::STORE;
  return Mode::IDLE;
}

static float readHvBusVolts() {
  // BENCH: calibrate divider ratio + ADC nonlinearity against a HV meter.
  const float SCALE = 0.147f; // placeholder
  return analogRead(PIN_HV_SENSE) * SCALE;
}

// BENCH: CAN shims. car_awake = any traffic heard on branch A within 2 s.
// be_heartbeat + pack current = Battery-Emulator status frames on branch B.
// motion = wheel-speed broadcast from the followdrive controller.
static bool canA_activity()        { return false; /* TWAI RX timestamp check */ }
static bool canB_beHeartbeat()     { return false; }
static bool canB_motion()          { return false; }
static float canB_packCurrentA(bool& valid) { valid = false; return 0; }
static void canB_requestContactorsOpen() { /* BE open-contactors frame */ }
static void broadcastStatus(const Outputs& o) { /* 1 Hz state frame on trailer CAN */ }

void setup() {
  pinMode(PIN_SEL_CAMP, INPUT_PULLUP); pinMode(PIN_SEL_DRIVE, INPUT_PULLUP);
  pinMode(PIN_SEL_STORE, INPUT_PULLUP); pinMode(PIN_7PIN_SENSE, INPUT);
  pinMode(PIN_ESTOP, INPUT_PULLUP); pinMode(PIN_FAULT_RESET, INPUT_PULLUP);
  pinMode(PIN_RELAY_ENGAGE, OUTPUT); pinMode(PIN_RELAY_SELECT, OUTPUT);
  pinMode(PIN_CAR_LV_GATE, OUTPUT); pinMode(PIN_ALARM, OUTPUT);
  // power-on state = nobody is master (relays default open = safe by wiring, not code)
  digitalWrite(PIN_RELAY_ENGAGE, LOW); digitalWrite(PIN_CAR_LV_GATE, LOW);
  Serial.begin(115200);
}

void loop() {
  Inputs in;
  in.now_ms = millis();
  in.selector = readSelector();               // TODO: 50 ms debounce
  in.hv_bus_v = readHvBusVolts();
  in.pack_current_a = canB_packCurrentA(in.pack_current_valid);
  in.seven_pin_present = digitalRead(PIN_7PIN_SENSE);
  in.motion = canB_motion();
  in.car_awake = canA_activity();
  in.be_heartbeat = canB_beHeartbeat();
  in.estop = digitalRead(PIN_ESTOP);          // NC loop opened
  in.fault_reset = !digitalRead(PIN_FAULT_RESET);

  const Outputs& o = sm.tick(in);

  digitalWrite(PIN_RELAY_ENGAGE, o.mux_engage);
  digitalWrite(PIN_RELAY_SELECT, o.mux_select_car);
  digitalWrite(PIN_CAR_LV_GATE, o.car_lv_power);
  digitalWrite(PIN_ALARM, o.alarm);
  if (o.request_be_open_contactors) canB_requestContactorsOpen();
  broadcastStatus(o);
  delay(20); // 50 Hz is plenty; the sequence lives in seconds
}
