# Flagship-First Build Plan — v0.2

**Date:** 2026-07-08 | **Owner:** TJ | **Supersedes:** build order in `PROJECT-SLIPSTREAM-Prototype-Roadmap.md` (that doc's V0.1→V1.0 arc and bench methods stand; the *article being built* changes)
**The pivot (TJ):** build the salvage Range-Neutral flagship FIRST — not the summer reference trailer. Salvage packs at $27/kWh are the moment; the reference build remains the configurator's default and a future kit, but Build #1 is the flagship.

## 1. Changed locked decisions (changelog against roadmap I.2)

| # | Was | Now | Why |
|---|---|---|---|
| D-F1 | 1,900 lb dry / Model Y | **≤3,500 lb LOADED, still behind the Model Y** | TJ: it must be pullable by the Y. The assist carries the load in motion; the 3,500 lb line keeps the hitch/brake/dead-battery story legal and honest |
| D-F2 | 12 kWh 48V LFP house pack | **NO 48V pack. 12V house spine fed by the donor PCS (~2.5 kW)** + ~100Ah 12V LFP buffer | The pack's own DC-DC ran the whole donor car; it's free, open-controlled (Maguire PCS board), and deletes 230 lb + $2.9K + two DC-DC rails |
| D-F3 | 12' box (reference) | **12' box, 15' fallback** | Weight math (§3) only closes at 12'; 15' triggers only if the pack+living layout physically fails — decide at CAD |
| D-F4 | Battery = 2170 LR assumption | **NICKEL NOW, first good donor wins** (Pack Memo v0.3): Track 1B nickel 2023–2025 LR/Standard co-primary with Track 1 LFP 2022–2024 M3 RWD; LFP breaks ties | TJ 2026-07-24: US ubiquity wins; 30–70% V2H band is degradation-gentle (~31 kWh/day); architecture chemistry-agnostic |
| D-F5 (rev. D-F2) | 12V spine as the power bus + MultiPlus 12/3000 | **Three-rail HV-first** (`HV_Power_Architecture_v0_1.md`): 400V DC bus for HV-native loads · ONE ~97% conversion via **trailer-mounted Solis** · 12V demoted to a ~500W control rail. **PCS keeps 11 kW AC charging + 12V rail** — two independent charge paths. MultiPlus deleted | TJ 2026-07-24: no double conversion, no 200A wiring; generator-mode V2H jumps 2.4 → ~10 kW |
| D-F6 | Open-controller cabin (window AC, tablet UI) | **Car-brain path (SS09 + SS09a):** same-donor nervous system — screen/Theater, native HVAC + Octovalve + Camp mode, NACS, rear + repeater cameras, app over Starlink Mini; **three-mode pack-master mux** (CAMP car-brain / DRIVE open stack / STORE BE+Solis), car-brain OFF outside CAMP | TJ 2026-07-24: native everything; donor spec refined — hail/rear hit, intact FRONT half, key cards at pickup |
| D-F7 | Build the full flagship in one go | **STAGED: V1 = nickel pack + wheels — camping + V2H energy trailer, NO truck drive/car-brain/cooling loop.** Rides the donor subframe with the DU pulled (V2 = bolt-in upgrade, no frame surgery). **V2 = DU + followdrive + car-brain + full thermal (+~382 lb → the §3-closed war).** DU/mux/controller develop on the bench in parallel, unhurried | TJ 2026-07-24: ship the energy trailer first; V1 nickel tows at 3,221 water-empty (−279) — even full-fresh is legal (−112). SS05b §5 |

Unchanged: pop-up soft-side, aero doctrine, composting head, outdoor shower, open-source everything, personal-cash cap discipline.

## 2. Flagship architecture (one page)

```
Salvage Tesla pack (LFP 60 or nickel ~78 kWh, sealed, stock BMS)
├── SS09a MODE MUX — pack has exactly ONE master at a time:
│     CAMP  → car-brain (gateway/VCFRONT/screen): native HVAC + Octovalve,
│             Camp mode, Theater, NACS charging, app via Starlink Mini
│     DRIVE → open stack: Maguire DU board + followdrive (hitch-force),
│             pump+radiator cooling (SS09a §1b), car-brain OFF
│     STORE → Battery-Emulator → Solis (V2H dispatch), car-brain OFF
├── 400V DC bus: rear DU e-axle · compressor (CAN-direct) · hydronic heater
├── Solis S6 (trailer-mounted): pack ↔ 240/120VAC (~97%, one conversion)
│     ├── induction / toaster / water heater · EVSE → charges the CAR ~7.6 kW
│     ├── solar DC-coupled into its MPPTs (series-string roof array)
│     └── V2H generator mode ~10 kW → house 50A inlet + interlock
├── PCS (in-pack): 11 kW AC charging (path #2) + 12V control rail (~2.5 kW avail)
└── 12V control rail: buffer 100Ah + lights, pumps, fans, sound, Starlink,
      actuators, brake/breakaway, SS09a supervisor  (~300-500W total)
```

**Load story (post-D-F5):** kW-class loads live on the Solis AC rail (97%, no ceiling worry at 10 kW class); the 2.5 kW PCS ceiling now only serves the ~300–500W control rail — 5–8× headroom. Cabin thermal is the donor heat pump (CAMP mode, more efficient than the deleted window AC). **Pack keep-alive** (contactors closed, 10–20W) runs 24/7 while camping — trivial, but stays in the model. Car-brain adds ~50–100W while awake in CAMP; zero in DRIVE/STORE (powered off).

## 3. Weight budget (the 3,500 lb war)

| Block | lb | Notes |
|---|---|---|
| Frame (12', tandem-ready single first) + belly + skid | 300 | SS05, designed AROUND the pack |
| Shell + pop-up (12' composite, 1" walls) | 380 | SS04 stack A/B |
| Salvage pack | 966–1,054 | LFP 966 / nickel +88 (first good donor wins) |
| Rear DU + subframe + controller + HV plumbing | 280 | SS07/SS05a |
| PCS in-pack; 12V buffer + Solis (trailer) + control-rail wiring | 135 | Solis 57 lb replaces MultiPlus 42; 12V fat wiring deleted |
| Suspension, wheels, brakes, hitch, jack, tongue | 320 | donor subframe IS the axle (SS05a) |
| Water (20 gal fresh + 10 gray, tanks) | 60 dry | water itself counts as payload |
| Interior: bed, galley, head, fixtures | 280 | foamie-informed lightweighting |
| Solar ~800W + mounts | 70 | series-string into Solis MPPTs |
| Systems misc + car-brain harvest (HVAC box, manifold, radiator, ECUs, screen, cameras, Starlink) | 220 | window AC deleted; SS09 adds ~80–120, partly offset |
| **DRY TOTAL** | **~3,030 (LFP) / ~3,120 (nickel)** | ⚠️ was 2,940 — the car-brain harvest bill |
| Payload budget (water 250 + gear/food) | 470–560 | weekend discipline, now chemistry-dependent |
| **LOADED** | **≤3,500 — HARD CAP** ⚠️ | **War status: on paper the nickel+car-brain combo eats ~150 lb of payload margin.** Offsets at CAD: interior −50 target, harvest trim (skip VCRIGHT-served items?), payload discipline. The cap never moves; payload flexes. Tongue ~310–350 lb — verify gray-empty case per SS05a |

**→ SUPERSEDED at component level by `engineering/SS05b_Mass_Budget.md` + `flagship_mass_budget.py` (2026-07-24):** honest inventory = dry ~3,205 LFP / ~3,293 nickel (fluids counted). War closes via the S1 strip list (−152, no capability loss) + **tow-empty water doctrine** (fresh tank fills at the campsite; −167 at the hitch): LFP tows at 3,363 (−137 ✓), nickel 3,451 (−49 ✓, S2 reserve −33 available). CAD carries CG + tongue live, as ever; balance solver re-run pending at these masses.

## 4. Build sequence (replaces reference-build V0.1 scope)

**Phase A — The organs (now → ~Q4 2026).** Donor acquisition per Guide #1 (target: 2021+ SR/RWD LFP, front/rear hit, Fremont). Pack commissioning per Guide #2. DU bench bring-up per Guide #3 (Maguire V3.2 — watch forum for field reports while bidding donors). PCS bring-up (12V rail + shore charging) on the bench — this validates D-F2 before the trailer exists. **Gate A (expanded for D-F5/D-F6):** pack ≥80% SoH commissioned + DU spins under openinverter + PCS delivers 2 kW+ at 12V for 1 hr **+ car-brain boots on the bench (screen + HVAC live in Camp mode) + BMS wake verified under BOTH masters through the SS09a mux + Octovalve parks for drive mode + salvage-VIN ownership transfer initiated with Tesla + Solis follows Battery-Emulator on the bench pack.**
**Phase B — The controller (parallel).** Patent design-around review (US 11,642,970 / 12,162,363 family) → hitch-force controller prototype on the bench rig: load cell + IMU + torque commands to the benched DU. **Gate B:** closed-loop force-following demo on the bench.
**Phase C — The V1 vehicle (after A, per D-F7).** Frame CAD around the pack (SS05: pack IS the skateboard; subframe bosses designed in, DU absent), shell per SS04, aero per SS06. Rolling chassis + pack + subframe-no-DU + Solis + camping fit-out. **Gate C = V1 SHIPS:** tows behind the Model Y directly (2,911 dry needs no assist), camps, charges at 11 kW, and does its first V2H session at the house. V1 is a complete usable product, not a milestone.
**Phase D — The V2 upgrade (drive integration).** DU bolts into the waiting subframe + halfshafts + HV branches + car-brain install + coolant/refrigerant loops + SS09a mux goes live. Assist behind the Y, graduated testing. **Gate D = the money gate:** 200-mile mixed loop at ≤5% net range loss, every fail-safe (force-sensor fault, CAN loss, 7-pin pull) drops to free-wheel cleanly.

## 5. Budget delta vs the old plan

Deletions: EVE pack system (−$2.9K), 48V MultiPlus + DC-DCs (−$1.7K). Additions: donor all-in ~$5–6K (recoup $2–5K part-out), Maguire boards ~$500–800, buffer+12V inverter ~$1.4K, controller dev ~$800, HV plumbing ~$750. **Net: flagship Build #1 lands ~$21–28K in components** — comparable to the old V0.1+V0.5 arc, for the top-tier article. Cash cap discipline unchanged.

## 6. Honest risks (new ones this pivot creates)

1. **Tongue weight at 350 lb cap** — pack placement fore/aft is the design's hardest constraint; aft-of-axle pack bias pre-engineered (old risk R1, doubled)
2. **PCS single-point dependency** — house power dies if the PCS dies; buffer battery + portable jump path mitigates; bench-validate hard in Phase A
3. **V3.2 tester-grade** — no independent field reports yet; Phase A benching IS the field report; T2-C is NOT a fallback for headless trailer duty (Guide #3)
4. **Dead-battery towing** — 3,400+ lb loaded with assist offline exceeds the Y's comfort; contingency = discharge-limited return legs + the 3,500 line existing for exactly this
5. **Model Y hitch/brake legalities** — loaded-at-rating is legal; the assist makes it *nicer*, not *more legal* — stay at/under 3,500 loaded, period
6. **Insurance/registration** (SS08 gray zones) — engage early, document, publish
7. **Highland PCS unproven with the open controller** (split-donor consequence): the 12V control rail and 11 kW shore charging both ride on the donor PCS; on a 2024-2025 pack donor neither is demonstrated yet. Phase-A bench gate tests exactly this; fallback = Elcon TC 6.6 kW charger + industrial 400→12V DC-DC (~1-2 kW) + larger 12V buffer — AND the trailer Solis is now a second full charge path, shrinking this risk. DU comes from the proven 2021-2023 pool regardless
8. **Salvage-VIN app access** (D-F6): basic app tier (climate/Camp/SoC) expected after ownership transfer but not guaranteed; Sentry Live needs Premium Connectivity, which Tesla may refuse on salvage. Mitigation: local USB Sentry recording always works; start the transfer process the week the donor lands; worst case one IP cam on the Starlink WiFi
9. **Weight pressure from the car-brain harvest** (D-F6): ~80–120 lb added; nickel adds up to another 88. On paper the loaded margin thins to ~0 with full payload — the §3 war status. CAD + corner-weigh decide; if it doesn't close, the trim order is: harvest extras first, interior second, payload discipline third. The 3,500 cap is never the variable
10. **Mode-mux is unproven anywhere** (SS09a): BMS wake choreography under two masters is the gating unknown; it's a $0 bench test on donor day one, and the whole design keeps "nobody is master" as a safe idle state

*v0.2 (2026-07-24; v0.1 2026-07-08). Feeds: SS02 (control-rail variant), SS05 (frame-around-pack), SS07 (Build #1), SS09/SS09a (car-brain + mux), HV_Power_Architecture memo, configurator (hv_hybrid option). The reference summer build remains the configurator default and future kit — this doc changes what TJ builds, not what Slipstream offers.*
