# Flagship-First Build Plan — v0.1

**Date:** 2026-07-08 | **Owner:** TJ | **Supersedes:** build order in `PROJECT-SLIPSTREAM-Prototype-Roadmap.md` (that doc's V0.1→V1.0 arc and bench methods stand; the *article being built* changes)
**The pivot (TJ):** build the salvage Range-Neutral flagship FIRST — not the summer reference trailer. Salvage packs at $27/kWh are the moment; the reference build remains the configurator's default and a future kit, but Build #1 is the flagship.

## 1. Changed locked decisions (changelog against roadmap I.2)

| # | Was | Now | Why |
|---|---|---|---|
| D-F1 | 1,900 lb dry / Model Y | **≤3,500 lb LOADED, still behind the Model Y** | TJ: it must be pullable by the Y. The assist carries the load in motion; the 3,500 lb line keeps the hitch/brake/dead-battery story legal and honest |
| D-F2 | 12 kWh 48V LFP house pack | **NO 48V pack. 12V house spine fed by the donor PCS (~2.5 kW)** + ~100Ah 12V LFP buffer | The pack's own DC-DC ran the whole donor car; it's free, open-controlled (Maguire PCS board), and deletes 230 lb + $2.9K + two DC-DC rails |
| D-F3 | 12' box (reference) | **12' box, 15' fallback** | Weight math (§3) only closes at 12'; 15' triggers only if the pack+living layout physically fails — decide at CAD |
| D-F4 | Battery = 2170 LR assumption | **CATL LFP Gen2 60 kWh — 2022–2024 Model 3 RWD donor** (Pack Selection Memo 2026-07-10: newest US LFP that exists; same pack design ships new in Canada 2026) | 88 lb lighter, cheaper, safer chemistry, happy parked at 100%; 60 kWh is plenty for assist + house + V2H. Fallbacks ranked: Mach-E SR LFP (72 kWh, costs the PCS spine) → LR 2170 NCA (abundant, 60–80% SoC discipline) |

Unchanged: pop-up soft-side, aero doctrine, composting head, outdoor shower, open-source everything, personal-cash cap discipline.

## 2. Flagship architecture (one page)

```
CATL LFP salvage pack (~340V, 55-60 kWh, 966 lb, sealed, stock BMS)
├── Battery-Emulator (CAN master for pack)
├── Rear DU e-axle ── Maguire V3.2 board ── hitch-force controller (headless torque)
├── PCS ── Maguire PCS board:
│     ├── shore/dock AC in → ~11 kW pack charging (NEMA 14-50)
│     └── 12V DC-DC out (~2.5 kW) → THE HOUSE SPINE
├── 12V spine: buffer battery (100Ah LFP) + fridge, lights, pumps, fans,
│     actuators (PA-17 12V config), Cerbo GX (12V), MPPT (solar→12V buffer)
├── 12V→120V inverter (MultiPlus 12/3000 class) → AC, induction, water heater
│     └── house-feed mode → V2H Tier 1 (generator inlet + interlock)
└── Winter: pack docks to house Solis inverter (V2H Tier 2);
      trailer hibernates on buffer + solar
```

**Load budget vs the 2.5 kW PCS ceiling:** window AC ~450W + fridge 45W + 12V misc 30W ≈ 525W typical evening — 5× headroom. Peaks (water heater 1.2 kW or induction 1.8 kW via inverter) get load-managed by the Cerbo (never simultaneous with AC at full PCS draw). Hot-night math: 12 hr AC ≈ 5.4 kWh from 55,000 Wh — the pack doesn't notice. **Pack keep-alive** (contactors closed, 10–20W) runs 24/7 while camping — trivial against 55 kWh but must be in the model.

## 3. Weight budget (the 3,500 lb war)

| Block | lb | Notes |
|---|---|---|
| Frame (12', tandem-ready single first) + belly + skid | 300 | SS05, designed AROUND the pack |
| Shell + pop-up (12' composite, 1" walls) | 380 | SS04 stack A/B |
| CATL LFP pack | 966 | The anchor. LR 2170 (+88) only if LFP donors dry up |
| Rear DU + mounts + controller + HV plumbing | 280 | SS07 |
| PCS is in-pack; 12V buffer + inverter + spine wiring | 120 | replaces 275 lb of 48V system |
| Suspension, wheels, brakes, hitch, jack, tongue | 320 | Timbren class, brakes on axle(s) |
| Water (20 gal fresh + 10 gray, tanks) | 60 dry | water itself counts as payload |
| Interior: bed, galley, head, fixtures | 280 | foamie-informed lightweighting |
| Solar ~800W + mounts | 70 | slightly reduced array |
| Systems misc (AC unit, heater tank, fans, lights) | 160 | |
| **DRY TOTAL** | **~2,940** | |
| Payload budget (water 250 + gear/food ~310) | 560 | weekend discipline |
| **LOADED** | **≤3,500** ✅ | tongue ~10-11% ≈ 350 lb = exactly the Y's cap — **tongue management is the #2 war after weight** |

Every SS-track mass line gets re-baselined to this table. CAD carries CG + tongue live, as ever.

## 4. Build sequence (replaces reference-build V0.1 scope)

**Phase A — The organs (now → ~Q4 2026).** Donor acquisition per Guide #1 (target: 2021+ SR/RWD LFP, front/rear hit, Fremont). Pack commissioning per Guide #2. DU bench bring-up per Guide #3 (Maguire V3.2 — watch forum for field reports while bidding donors). PCS bring-up (12V rail + shore charging) on the bench — this validates D-F2 before the trailer exists. **Gate A:** pack ≥80% SoH commissioned + DU spins under openinverter + PCS delivers 2 kW+ at 12V for 1 hr.
**Phase B — The controller (parallel).** Patent design-around review (US 11,642,970 / 12,162,363 family) → hitch-force controller prototype on the bench rig: load cell + IMU + torque commands to the benched DU. **Gate B:** closed-loop force-following demo on the bench.
**Phase C — The vehicle (after A).** Frame CAD around the pack (SS05 rework: pack IS the skateboard), shell per SS04 samples, aero per SS06 (frontal geometry unchanged — CFD matrix stands). Rolling chassis + pack + DU install. **Gate C:** rolls, brakes, tows dead (assist off) behind a bigger tug at low speed.
**Phase D — Integration.** Assist active behind the Model Y, graduated speed/load testing, V2H Tier 1 at home. **Gate D = the money gate:** Model Y tows the loaded flagship on the 200-mile mixed loop at ≤5% net range loss, and every fail-safe (force-sensor fault, CAN loss, 7-pin pull) drops to free-wheel cleanly.

## 5. Budget delta vs the old plan

Deletions: EVE pack system (−$2.9K), 48V MultiPlus + DC-DCs (−$1.7K). Additions: donor all-in ~$5–6K (recoup $2–5K part-out), Maguire boards ~$500–800, buffer+12V inverter ~$1.4K, controller dev ~$800, HV plumbing ~$750. **Net: flagship Build #1 lands ~$21–28K in components** — comparable to the old V0.1+V0.5 arc, for the top-tier article. Cash cap discipline unchanged.

## 6. Honest risks (new ones this pivot creates)

1. **Tongue weight at 350 lb cap** — pack placement fore/aft is the design's hardest constraint; aft-of-axle pack bias pre-engineered (old risk R1, doubled)
2. **PCS single-point dependency** — house power dies if the PCS dies; buffer battery + portable jump path mitigates; bench-validate hard in Phase A
3. **V3.2 tester-grade** — no independent field reports yet; Phase A benching IS the field report; T2-C is NOT a fallback for headless trailer duty (Guide #3)
4. **Dead-battery towing** — 3,400+ lb loaded with assist offline exceeds the Y's comfort; contingency = discharge-limited return legs + the 3,500 line existing for exactly this
5. **Model Y hitch/brake legalities** — loaded-at-rating is legal; the assist makes it *nicer*, not *more legal* — stay at/under 3,500 loaded, period
6. **Insurance/registration** (SS08 gray zones) — engage early, document, publish
7. **Highland PCS unproven with the open controller** (split-donor consequence): the 12V house spine and 11 kW shore charging both ride on the donor PCS; on a 2024-2025 pack donor neither is demonstrated yet. Phase-A bench gate tests exactly this; fallback = Elcon TC 6.6 kW charger + industrial 400→12V DC-DC (~1-2 kW) + larger 12V buffer. DU comes from the proven 2021-2023 pool regardless

*v0.1. Feeds: SS02 (12V spine variant), SS05 (frame-around-pack), SS07 (now Build #1, gate removed), configurator (no-48V-pack option). The reference summer build remains the configurator default and future kit — this doc changes what TJ builds, not what Slipstream offers.*
