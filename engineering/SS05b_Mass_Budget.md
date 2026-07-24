# SS05b — Component Mass Budget & Weight-Recovery Plan · Design Track

**Status:** v0.1 (pre-scale estimates) | **Parent:** SS05/SS05a | **Model:** `flagship_mass_budget.py` (the numbers live in code — this doc is its narrative; rerun the script after any change)
**Trigger:** TJ 2026-07-24 — full component inventory including fluids, then strip weight.

## 1. The honest roll-up (and the bad news first)

Component-level accounting lands **heavier than the Flagship Plan §3 coarse budget**: ~3,205 lb dry (LFP) vs the plan's ~3,030. The extra ~175 lb was hiding in drive-line detail (halfshafts, brakes, hitch hardware), plumbing detail, and fluids nobody had counted (30 lb of coolant, refrigerant, brake fluid). Coarse budgets always flatter; this is why the inventory exists.

| Category | lb (LFP baseline) |
|---|---|
| Structure (frame/belly/skid + shell/pop-up) | 680 |
| Drive & running gear (DU+subframe 480, wheels 120, brakes/hitch/jack) | 675 |
| Energy (pack 966, Solis 66, buffer 28, HV+LV wiring 65) | 1,125 |
| Car-brain harvest (screen/ECUs/HVAC box/manifold/radiator/harness…) | 178 |
| Fluids (coolant 25, refrigerant 3, brake fluid 2) | 30 |
| Water & plumbing, dry (tanks, heater, head, shower) | 105 |
| Interior (bed, galley+fridge, cabinetry, floor) | 280 |
| Systems (solar 70, actuators 30, Starlink, fans, sound, electronics) | 132 |
| **DRY TOTAL** | **3,205 LFP / 3,293 nickel (+88)** |

**Baseline war status (payload = 310 gear + 167 full fresh water):** every towing scenario is over cap — LFP full-fresh +182, nickel full-fresh +270, even LFP water-empty +15. Unstripped, this trailer does not legally leave the driveway behind the Y.

## 2. The two moves that win it

### Move 1 — S1 strip list: −152 lb, zero capability lost

| Save | Item | How |
|---|---|---|
| −40 | Solar | semi-rigid lightweight panels + bonded rails (~30 lb total vs 70 rigid) |
| −25 | Water heater | **DELETE the 120V tank** — the 400V hydronic loop (HV memo) already does shower + space heat |
| −24 | Wheels/tires | aftermarket flow-formed 18" pair (~48 lb/pair vs donor ~72) |
| −20 | Cabinetry | CNC-lightened panels, foam-core doors — foamie tech flowing UP the tier ladder |
| −15 | Bed | lightweight foam + slat platform |
| −10 | Harness | trim to length at the bench, strip unused branches (copper is heavy) |
| −6 ×3 | Jack / induction / sound | aluminum jack · portable induction · BT speaker rides as payload |

### Move 2 — Tow-empty water doctrine: −167 lb at the hitch, $0

The 3,500 cap applies **while towing**. Gray water must be dumped before towing anyway; extend the rule: **tow with the fresh tank empty too — fill at the campsite or last stop.** Water becomes camp-only payload. This is discipline, not hardware, and it's the single biggest lever on the sheet.

## 3. War status after both moves

| Scenario | Weight | vs 3,500 cap |
|---|---|---|
| **LFP + S1, tow water-empty** | **3,363** | **−137 ✓ comfortable** |
| LFP + S1, tow full-fresh (violates doctrine) | 3,530 | +30 — at cap, don't |
| **Nickel + S1, tow water-empty** | **3,451** | **−49 ✓ thin but legal** |
| Nickel + S1, tow full-fresh | 3,618 | +118 ✗ |

**Verdict: the war closes for BOTH chemistries** with S1 + tow-empty water. Nickel's 49 lb margin is thin — if CAD confirms it, the S2 reserve (−33 lb: 15-gal fresh tank, lighter dry toilet, manual pop-up) buys it back to −82. S3 (gutting the cabin HVAC box for a custom air handler, −20) stays untouched — it would wound the native Camp mode that D-F6 exists for.

## 4. Standing rules

1. **The mass model lives in `flagship_mass_budget.py`** — change the build, change the code, rerun. Same doctrine as the balance solver (which must be re-run at these masses: axle/pack placement shifts, tongue target 310–350).
2. Every number here is a pre-scale estimate; the first bathroom-scale session on real donor parts re-baselines the file, line by line — cheap and mandatory during teardown (weigh EVERYTHING as it comes off).
3. LFP's tiebreaker value just went up again: the −88 lb is nearly double nickel's post-S1 margin. Worth remembering on auction day when the two tracks tie.
4. Payload discipline is design-load 310 lb of gear — the configurator and the manual say so out loud.

## 5. V1 staged build (TJ, 2026-07-24): the war doesn't even start until V2

**V1 = nickel pack + wheels. No truck drive, no car-brain, no cooling loop** (passive pack: 11 kW charging = 0.14C on 78 kWh — benign; verify at commissioning). Camping + V2H energy trailer first; the drive system, car-brain, and full thermal loop are the **V2 upgrade** (~+382 lb, which lands exactly on the full-flagship war already closed in §3).

### The branch matrix (both branches × both chemistries; subframe-no-DU route)

| Scenario | Dry | Tow water-empty | Tow full-fresh | Camp static* |
|---|---|---|---|---|
| **V1 LFP** | 2,823 | 3,133 (−367 ✓) | 3,300 (−200 ✓) | 3,383 |
| V1 LFP + S1 | 2,696 | 3,006 (−494 ✓) | 3,173 (−327 ✓) | 3,256 |
| **V1 nickel** (the likely build) | 2,911 | 3,221 (−279 ✓) | 3,388 (−112 ✓) | 3,471 |
| V1 nickel + S1 | 2,784 | 3,094 (−406 ✓) | 3,261 (−239 ✓) | 3,344 |
| V2 LFP base | 3,205 | 3,515 (+15 ✗) | 3,682 (+182 ✗) | 3,765 |
| **V2 LFP + S1** | 3,053 | 3,363 (−137 ✓) | 3,530 (+30 ✗) | 3,613 |
| V2 nickel base | 3,293 | 3,603 (+103 ✗) | 3,770 (+270 ✗) | 3,853 |
| **V2 nickel + S1** | 3,141 | 3,451 (−49 ✓) | 3,618 (+118 ✗) | 3,701 |

*Camp static (gear + full fresh + full gray) has no towing cap — it's a GAWR question: at V2 nickel's 3,853 static, the axle sees ~3,450+ vs the donor's ~2,600 lb/axle duty. **The SS05a spring/bearing upgrade flag is now driven by the CAMP case, not the tow case** — carry that into CAD.

Reading the matrix: **V1 is unconditionally legal** — both chemistries, stripped or not, even towing full water. **V2 is only legal with S1 applied AND the tow-empty water doctrine** — S1 stops being optional the day the DU bolts in, so do the S1 items during the V1 build (they're cheaper to do once than to retrofit). Alternate Timbren axle route for V1 (rejected): −170 lb more but makes V2 frame surgery.

**Axle recommendation: ride the donor subframe with the DU pulled.** It costs 170 lb of margin V1 doesn't need (still −279, and even full-fresh towing is legal — the tow-empty doctrine becomes optional for V1), and it buys: V2 = *bolt the DU in* instead of frame surgery, skirted-wheel aero from day one, donor brakes + EPB retained, identical axle geometry so the balance solves once, and the part is free with the donor. Meanwhile the DU develops on the bench, unhurried — which is where it was going anyway. V1 water heat = 120V tankless off the Solis (the hydronic loop arrives with V2's coolant system).

---
*v0.1, 2026-07-24. Supersedes Flagship Plan §3 numbers (plan v0.2 re-pointed here). Feeds SS05 CAD (mass targets per category are now line items, not vibes) and flagship_balance.py re-run — including the V1 no-DU rear-mass case.*
