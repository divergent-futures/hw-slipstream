# SS09 — Car-Brain Path: Donor Nervous-System Harvest · Design Track

**Status:** v0.1 manifest | **Trigger:** TJ 2026-07-24 — keep native NACS charging, Tesla HVAC (Octovalve loop, cabin + pack cooling), Camp/Dog/Keep modes, and the screen (HVAC UI + YouTube/Netflix)
**Governs:** Guide #1 teardown keep-list (extends it), Guide #2 (pack side unchanged), the CAN-mux design (open item #1)

## 0. The one rule that generates this whole list

Tesla ECUs are **VIN-married** (Toolbox-programmed to the car's config, which lives in the gateway). Mixing modules from different donors = "incorrect configuration" hell or a Toolbox session. Therefore: **every module below comes from the SAME donor as the pack.** This strengthens the single-good-donor-wins policy — the ideal donor is now hail/rear with an intact FRONT half.

Power sequencing is a chain: **VCFRONT powers VCLEFT powers VCSEC** — you cannot cherry-pick "just the screen."

## 1. Harvest manifest, by function

### A. Compute + UI (the screen story)
- **Car Computer** (one enclosure: infotainment MCU + integrated **gateway** + Autopilot HW board — the AP board rides along, now also serving the kept cameras; the gateway holds the car config = the marriage license)
- **Touchscreen** + its harness run
- **WiFi/LTE antennas** (YouTube/Netflix = Theater mode, runs over WiFi, in Park — no premium connectivity needed)
- **Cabin temp + humidity sensor** (windshield header) — HVAC auto mode is blind without it
- Interior camera not needed; expect a fault line, cosmetic only

### A2. Cameras + connectivity (TJ, 2026-07-24: keep native app usage)
- **KEEP: rear camera + both side repeater cameras** (fender units) — remounted on the trailer (repeaters at front corners, rear at the hatch). They feed the AP board we're keeping anyway. **SKIP: front windshield trio + B-pillar cameras** — their absence adds AP fault lines, cosmetic.
- **Starlink Mini, permanently installed, on the 12V control rail** — native 12–48V DC input, ~25–40W (~0.6–1 kWh/day, trivial against the pack). It's the trailer's WiFi: the car-brain connects like a car parked in a garage, so app reachability continues while out hiking.
- **App-access reality (verified 2026-07):** ownership transfer on a salvage title = submit bill of sale + salvage title via Tesla support → app access is usually granted, but Tesla can refuse app/Premium Connectivity/Supercharging on salvage VINs — not guaranteed. Basic app tier (climate/Camp mode control, SoC, lock, location) needs no subscription. **Sentry Mode LIVE camera view requires Premium Connectivity ($9.99/mo) even on WiFi** — and premium on a salvage VIN is exactly what Tesla may refuse. Guaranteed fallback regardless: Sentry/dashcam records locally to USB and plays back on the screen; worst-case remote view = one cheap IP cam on the Starlink WiFi.

### B. Body controllers + security (the wake/auth story)
- **VCFRONT** — power distribution (it IS the fuse box), front thermal control (drives the Octovalve stepper + coolant valves — service-manual test "TEST-SELF_VCFRONT_FIVE-WAY-VALVE" confirms), fans, pumps
- **VCLEFT + VCRIGHT** — body LIN/CAN endpoints; VCLEFT is in the VCSEC power chain
- **VCSEC** + B-pillar NFC reader + center-console NFC reader + BLE antennas — wake, auth, alarm
- **THE DONOR'S KEY CARDS** — ask the yard, check the glovebox/console AT PICKUP. Without a paired key, first wake needs a Toolbox session. This goes on the auction-day checklist.

### C. Thermal (the Octovalve story — pack AND cabin)
- **Supermanifold + Octovalve** (the whole assembly, unsplit)
- **Compressor** (CAN, HV-powered)
- **Cabin HVAC box** — blower, evaporator, cabin condenser, air-distribution doors (the full dash unit; Camp mode is this box + VCFRONT + screen)
- **Both coolant pumps, radiator + fan shroud, chiller, refrigerant/pressure/temp sensors**, plumbed per the donor loop (pack cooling and cabin cooling are ONE system — that's the point of the Octovalve)

### D. Charging (the native-NACS story)
- **Charge port assembly** — inlet + latch + LEDs + charge-port ECU
- **PCS** (in-pack penthouse, already core) — 11 kW AC charging + 12V DC-DC
- HV charge harness run from port to penthouse

### E. Low voltage
- **Donor LV battery** (lithium aux) + front-harness sections, as intact as practical (harvest generously at teardown — connectors are the expensive part to recreate)

### F. Already core (unchanged)
Pack + BMS + pyro + contactors + HVIL; rear DU + subframe (SS05a); Battery-Emulator + Solis (storage mode).

## 2. What will complain, and what it costs

Missing ABS/iBooster, restraints (airbag ECU), seatbelts, front/pillar cameras → the screen will carry standing alerts. **None of them block HVAC, Camp mode, Theater mode, or charging** — the car happily heats, cools, streams, and charges while "parked." Optional cosmetics later: keep the restraint module powered to quiet the loudest alerts. Camp mode requires >15% SoC (Tesla software rule) — irrelevant in practice with V2H dock discipline.

## 3. The two-brain reality (open item #1 — the invention)

In **cabin mode** the car-brain owns the pack (BMS, contactors, thermal, charging). In **storage/dock mode** Battery-Emulator must own it for the Solis. One organ, one master: a **CAN changeover (physical mux) between the pack CAN and the two masters**, with a clean handoff sequence (car asleep → contactors open → mux flips → BE session). Nobody has published this. It is simple hardware + careful sequencing, it is the keystone of the whole TJ vision, and it is exactly the open-source contribution Slipstream should own. Design note to follow as SS09a.

## 4. Weight + budget flags

Adds roughly 80–120 lb (HVAC box, manifold, radiator, ECUs, harness) against the flagship's "systems misc" 160 lb line — re-baseline at SS05 corner-weigh. Cost ≈ $0 marginal (it all rides in the one donor) — the harvest cost is teardown HOURS and careful connector discipline. The deleted items it displaces: RecPro-class heat pump (~$1,200) and window AC — the donor HVAC is better hardware than either. Starlink Mini hardware ~$599 + Roam service (TJ's line item).

## 5. Open questions

1. CAN mux + handoff sequence (SS09a) — THE gating design
2. Does Camp mode run with drive-unit faults present? (expected yes — verify on bench, add to Gate A tests)
3. Keeping the car-brain 24/7 vs deep-sleep duty cycle: vampire drain on the pack (~1-3%/day car-awake vs ~0 in storage mode) — measure, publish
4. Highland (2024+) vs pre-Highland ECU topology differences — re-verify manifest if the donor is Highland
5. Salvage-title VIN: no OTA/account features assumed; confirm Theater/WiFi behavior on a benched salvage MCU early in Phase A
6. Ownership transfer + app association on the salvage VIN — start the Tesla support process the week the donor lands (docs: bill of sale + salvage title); test whether Premium Connectivity is purchasable on it (gates Sentry Live remote view)
7. Does Sentry/dashcam record with only rear + repeaters present (no front trio)? Bench-verify; expected yes with fault lines
8. Camera remount optics: repeater/rear housings are shaped for car body panels — design flush trailer mounts (SS04 shell detail); keep cable runs inside the donor harness lengths

---
*v0.1, 2026-07-24. Sources: TMC "Model 3 MCU on the bench", Tesla Owners Online scratch-build thread (module list + VCFRONT→VCLEFT→VCSEC power chain, VIN/Toolbox marriage), Tesla service manual (VCFRONT coolant-valve self-test, Octovalve R&R), openinverter compressor CAN docs, TMC/owners forums on salvage ownership transfer + Sentry Live premium requirement. Everything above is superseded by the first bench session with real hardware.*
