# V1 / V2 Component Checklist — v0.1 (granular)

**Date:** 2026-07-24 | **Companions:** `engineering/flagship_mass_budget.py` (weights), `engineering/SS05b_Mass_Budget.md` (war status), Guide #1 (teardown), `engineering/SS09_Donor_Nervous_System.design.md` (harvest manifest)
**Legend — source codes:** `[A]` harvest from Donor A (pack donor: rear-hit/hail, FRONT INTACT) · `[B]` Donor B / recycler (mechanical) · `[BUY]` purchase · `[BUILD]` fabricate · `[SHELF]` harvest at Donor-A teardown, store for V2
Checkboxes are GitHub-renderable — check them off as parts land.

---

## PART 1 — V1 BUILD (energy trailer: camp + charge + V2H; no drive, no car-brain)

### 1A. Donor A harvest — use now
- [ ] `[A]` **HV battery pack, complete & sealed** — penthouse (PCS + pyro + contactors + BMS) intact, never opened · ~1,054 lb (nickel) / 966 (LFP)
- [ ] `[A]` **Charge port assembly** — NACS inlet + latch + LEDs + charge-port ECU · 8 lb
- [ ] `[A]` **KEY CARDS** — glovebox + center console AT PICKUP (no card = Toolbox session later)
- [ ] `[A]` Donor wheels + tires, best pair · 120 lb (V1 rolls on these; flow-formed pair is an S1 swap later)
- [ ] `[A]` HV cable sections + orange loom + glands (harvest generously — connectors cost real money)

### 1B. Donor A harvest — SHELF FOR V2 (one teardown, label everything, photograph everything)
- [ ] `[SHELF]` Car Computer (infotainment + gateway + AP board, one enclosure) + touchscreen
- [ ] `[SHELF]` VCFRONT · VCLEFT · VCRIGHT · VCSEC + NFC readers (B-pillar + console) + BLE antennas
- [ ] `[SHELF]` Cabin temp + humidity sensor (windshield header)
- [ ] `[SHELF]` HVAC box complete (blower, evap, cabin condenser, air doors)
- [ ] `[SHELF]` Supermanifold + Octovalve + chiller — unsplit, capped, bagged
- [ ] `[SHELF]` HV compressor + its HV pigtail
- [ ] `[SHELF]` Radiator + fan + shroud · both coolant pumps · refrigerant/pressure/temp sensors
- [ ] `[SHELF]` Rear camera + both side repeater cameras + pigtails
- [ ] `[SHELF]` LV lithium aux battery
- [ ] `[SHELF]` Front harness sections, cut LONG (trim at bench, never at teardown)
- [ ] `[A]` Part-out for offset: doors, glass, lights, seats, remaining wheels ($2-5K recovery target)

### 1C. Donor B / recycler — mechanical
- [ ] `[B]` **Rear subframe assembly, complete** — arms, knuckles, hubs, springs, dampers, calipers + EPB, halfshafts · ~300 lb without DU (recycler $300-800, or front-hit donor)
- [ ] `[B]` (opportunistic) DU cheap? Buy and shelve for V2 bench · +180 lb, $1,500-2,500

### 1D. Buy — HV electrical
- [ ] `[BUY]` Battery-Emulator hardware (LilyGo T-2CAN) · $70
- [ ] `[BUY]` Maguire open PCS controller board · $120 (12V rail + 11 kW AC charging)
- [ ] `[BUY]` **Solis S6-EH1P11.4K-H-US** hybrid inverter · $2,400 · 58 lb
- [ ] `[BUILD]` Solis isolation mount (plate + elastomer isolators) · 8 lb
- [ ] `[BUY]` X098 pack-connector pigtail/plug · $60
- [ ] `[BUY]` HV service disconnect + Class-T/EV fuse + holder · $150
- [ ] `[BUY]` HV cable 35 mm² orange (what Donor A didn't yield), lugs, glands · $150
- [ ] `[BUY]` HVIL loop wire + connectors (60 Ω RWD / 120 Ω AWD termination per X098 doctrine)
- [ ] `[BUY]` NEMA 14-50 inlet (trailer shore-in) + 25' cordset · $180
- [ ] `[BUY]` House-side kit: 14-50 inlet + panel interlock + NEC 702.7(C) signage · $500
- [ ] `[BUY]` Portable EVSE 240V/32A (pack→car charging) · $250
- [ ] `[BUY]` (optional) isolation monitor (Bender-class IMD) · $200 — decide at commissioning

### 1E. Buy — 12V control rail
- [ ] `[BUY]` 12V 100Ah LFP buffer battery · $300 · 28 lb
- [ ] `[BUY]` Fuse panel, bus bars, master disconnect, 500A shunt monitor · $250
- [ ] `[BUY]` 12V loom: marine-grade wire, breakers, terminals · $150
- [ ] `[BUY]` Starlink Mini + 12V wiring + roof mount · $599 + Roam plan
- [ ] `[BUY]` Breakaway kit + battery + 7-pin harness · $60
- [ ] NOTE: **no modeswitch in V1** — Battery-Emulator is the sole pack master until the car-brain arrives. The mux is a V2 item.

### 1F. Buy — running gear & brakes
- [ ] `[BUY]` Electric-over-hydraulic brake actuator (Curt-Echo-compatible) · $400 · 12 lb
- [ ] `[BUY]` Brake lines, fittings, DOT4 fluid · $80
- [ ] `[BUY]` 2-5/16" coupler + **load-cell-ready mount machined now** (V2 provision, near-free at fab time) · $150 · 45 lb w/ tongue hardware
- [ ] `[BUY]` Aluminum tongue jack + caster · $90 · 12 lb
- [ ] `[BUY]` Spring/damper check parts per GAWR flag (SS05a): uprated coils or air springs — **decided at corner-weigh, budget $400-800**

### 1G. Build — structure (the aluminum frame around the pack)
- [ ] `[BUILD]` 6061 rect-tube frame, **designed around measured pack**, subframe bosses at x=120 axle line · ~300 lb w/ belly + skid (material ~$1,200)
- [ ] `[BUILD]` Skid plate under pack + penthouse (UHMW or 5052 alu)
- [ ] `[BUILD]` Belly fairing panels (pack edge → frame rails)
- [ ] `[BUILD]` Shell + pop-up, SS04 composite stack · ~380 lb (materials ~$2,500)
- [ ] `[BUILD]` Wheel skirts/fenders (foam-core per SS04)
- [ ] `[BUY]` Pop-up lift: 4× PA-17 actuators $600 · 30 lb — or manual + gas struts (S2: −22 lb, −$450)
- [ ] `[BUY]` Door + hatch hardware, seals, locks · $250

### 1H. Buy/build — camp systems
- [ ] `[BUY]` 800W semi-rigid solar (4 panels, series-strung ≥MPPT start V) + bonded rails · $700 · 30 lb (S1 spec from day one)
- [ ] `[BUY]` PV disconnect + MC4 + PV fusing · $80
- [ ] `[BUY]` 120V tankless water heater (V1 only — hydronic replaces it in V2) · $150 · 8 lb
- [ ] `[BUY]` 12V fridge 45L · $400 · Portable induction hob · $80 · Sink + faucet + 12V pump · $150
- [ ] `[BUILD]` Galley counter + CNC-lightened cabinetry (S1 spec) · ~166 lb total interior wood
- [ ] `[BUILD]` Bed platform (slats) + lightweight foam · 55 lb
- [ ] `[BUY]` Composting head · $900 · 28 lb · Outdoor shower kit · $100
- [ ] `[BUY]` Fresh 20 gal + gray 10 gal tanks, PEX, valves, fills, vents · $350
- [ ] `[BUY]` Maxxair fan + vents · $250 · LED lighting + USB-C outlets · $150
- [ ] `[BUY]` Safety: fire extinguisher (Class ABC + Class D awareness), smoke/CO, first aid · $150
- [ ] `[BUY]` HV PPE (Phase A list): Class-0 gloves + leathers + glove test dates, insulated tools, face shield, CAT III meter · $450

**V1 rollup: dry ~2,911 lb (nickel) · buy-cost ~$12-14K + Donor A ($5-9K, −$2-5K part-out) + subframe ($300-800)**

---

## PART 2 — V2 UPGRADE (truck drive + car-brain + full thermal)

### 2A. Drive system
- [ ] `[B]` Drive unit (if not already shelved) · 180 lb · $1,500-2,500
- [ ] `[BUY]` Maguire M3-DU logic board V3.2 · $500-800 (check field reports first)
- [ ] `[BUY]` ZombieVerter VCU (followdrive host) · $400
- [ ] `[BUY]` Load cell ±5,000 lbf + 24-bit CAN amplifier (NOT HX711) · $300
- [ ] `[BUY]` Automotive IMU + brake-signal optocoupler · $120
- [ ] `[BUILD]` Coupler load-cell integration (mount already machined in V1 — insert + calibrate)
- [ ] `[BUY]` DU HV branch: cable, fuse, connector · $200
- [ ] Halfshafts torque check, axle nuts, DU mounts/bushings → subframe

### 2B. Car-brain install (everything from the V1 shelf)
- [ ] `[SHELF→INSTALL]` Car Computer + screen (build enclosure/mount) · VCFRONT + VCLEFT + VCRIGHT + VCSEC + antennas + NFC readers
- [ ] `[SHELF→INSTALL]` Cabin temp/humidity sensor · rear + repeater cameras (flush trailer mounts, SS04 detail)
- [ ] `[SHELF→INSTALL]` LV aux battery · harness (TRIM TO LENGTH at bench — S1's −10 lb)
- [ ] `[ ]` Tesla ownership transfer done? Premium Connectivity attempt? (open items 6-7, SS09)

### 2C. Thermal (full loop goes live)
- [ ] `[SHELF→INSTALL]` HVAC box · supermanifold + Octovalve · compressor · radiator + fans · both pumps · sensors
- [ ] `[BUY]` Coolant (G48-class, ~3 gal) · $60 · 25 lb aboard
- [ ] `[BUY]` R1234yf charge + line crimp/vac/fill (shop service) · $250 · 3 lb
- [ ] `[BUY]` 400V coolant heater (salvage VW/Tesla-S class) + hydronic HX + mixing valve · $250 — **delete the V1 tankless (−8 lb)**
- [ ] `[BUY]` AC line stubs, fittings, dryer · $150

### 2D. Mode mux (SS09a — now there are two masters)
- [ ] `[BUY/BUILD]` modeswitch: ESP32 + 2× DPDT signal relays + isolated HV divider + 3-pos keyed selector + enclosure · ~$175 (firmware already in repo, tested)
- [ ] `[ ]` Bench: BMS wake choreography under BOTH masters (Gate A item — do before install)
- [ ] `[ ]` Octovalve park-position handoff verified

### 2E. Re-verify after upgrade (+~382 lb lands on the closed war)
- [ ] Corner-weigh → re-baseline `flagship_mass_budget.py` line by line
- [ ] `flagship_balance.py` re-run (tongue 310-350 target, gray-empty case)
- [ ] GAWR: springs/bearings vs ~3,450 lb camp-static axle load (the CAD hard requirement)
- [ ] S1 strip items all done? (they were built into V1 — verify none slipped)
- [ ] Tow-empty water doctrine now MANDATORY (V2 nickel margin = 49 lb)

---
*v0.1, 2026-07-24. Every weight/cost is a pre-scale, pre-quote estimate — the checklist is the shopping list, the mass model is the truth-keeper, the bathroom scale at teardown is the judge. Check items off in git so the build history is public.*
