# Slipstream Visual Design Prompts — v0.1

**Purpose:** keep the trailer looking like the SAME object across every render, and record what image generators get wrong so we stop re-learning it.
**Geometry source of truth:** `engineering/SS05a_Flagship_Frame_Layout.design.md` (12' box, 78" wide, 62.2" track fully inboard = skirted wheels) and `engineering/SS05b_Mass_Budget.md`.

## 1. The canonical description (paste this into any prompt)

- **12 feet long, 78 inches wide.** Tallest at the TOW-HITCH end (~5 ft, broad blunt rounded face); **dead-flat level roof**; tapers to a squared-off vertical tail (~3.5 ft) at the far end.
- **Wheels fully inside the body width and invisible.** Track (62.2") is narrower than the body (78"), so each flank is one flat unbroken plane. No arches, no fenders, no pods. ~10" shadow gap to the ground.
- Flush black solar panels lying flat on the roof; seamless matte sage-grey composite shell; dark charcoal band along the lower edge; one flush recessed door; A-frame tongue + ball coupler at the tall end.
- When hitched: roofline sits BELOW the tow vehicle's roof, body narrower than the car — it hides in the car's slipstream.

## 2. Failure log (2026-07-24 session, 8 renders)

| Failure | Why it happens | Fix that worked |
|---|---|---|
| **Built back-to-front** (tall end away from hitch) | "teardrop trailer" convention overrides "nose/tail" wording | Stop using nose/tail. Give **two heights**: "5 ft at the tow-hitch end, 3.5 ft at the far end" |
| **Domed / barrel roof** | generators default to curved caravan shells | "dead flat and level, like a table top", "a straight horizontal line in profile" |
| **Bare wheels + arches** | "skirted trailer wheels" isn't a known concept | Car references: Honda Insight / GM EV1 rear wheel spats |
| **Bulging wheel PODS** (the spat fix overshooting) | reads spats as bolt-on blisters | "each flank is one perfectly FLAT vertical plane… axle narrower than the body, wheels entirely INSIDE the width, nothing protrudes" |
| **Stubby proportions** | no scale anchor | Add "a six-foot person standing beside it for scale" — worked immediately |
| **Spurious fins/spoilers** | style drift | Explicit "no fins, no spoilers, no roof rack" |

## 0. THE REFERENCE IMAGE

**`docs/renders/slipstream_v1_reference_hero.jpg`** — the canonical look. Prompt 1C (Google Banana Pro) + one wheel-enclosure edit. Every future render is judged against it, and it should be fed back in as an image reference when generating new scenes so the object stays consistent. (`slipstream_v1_hero_prewheel-edit.jpg` is the same frame before the wheel edit — kept as the before/after record.)

## 2b. What finally worked (2026-07-24)

**Prompt 1C in Google "Banana Pro" produced the reference image** — correct orientation (tall blunt face at the hitch), flat roof, right length, squared tail, correct tongue/jack, scale person. Two conclusions:

1. **The two-heights trick is what fixed orientation** ("5 ft at the tow-hitch end, 3.5 ft at the far end"). Keep it in every prompt.
2. **Fix the last flaws by EDITING, not re-prompting.** Banana Pro edits conversationally and preserves the rest of the frame. Working edit for the recurring wheel problem:
   > Keep everything identical — same trailer, angle, lighting, person, background. Only change the wheel area: delete the wheel arch and the bulge around it. Extend the smooth side panel straight down so the flank becomes one continuous flat surface from front to tail, with no opening, no arch and no visible tyre. Keep the dark charcoal band unbroken along the bottom edge, leave a 10-inch shadow gap to the ground.

   Escalation if an arch survives: *"There should be no circular shape anywhere on the side of the trailer. The side is a single flat panel."*

## 3. Working prompt — hero exterior (v1E, current best)

> Photorealistic product photograph of a modern aerodynamic electric camping trailer, standalone on wet asphalt at dawn, overcast light, a six-foot person standing beside it for scale. SHAPE: tallest at the tow-hitch end — 5 feet high with a broad blunt rounded front face — then a dead-flat level roof running 12 feet straight back to a squared-off vertical tail 3.5 feet high. Four flush black solar panels lie flat on the roof. SIDES ARE CRITICAL: each flank is one perfectly FLAT vertical plane from front to back, like the side of a shipping container but smooth and seamless. There are NO wheel arches, NO fenders, NO bulging wheel pods, NO blisters and NO protrusions of any kind on the sides — nothing sticks out past the flat flank. The axle is narrower than the body, so both wheels sit entirely INSIDE the trailer's width, completely hidden behind the flat sides; no tyre or rim is visible from outside, only a 10-inch shadow gap between the bottom edge of the bodywork and the ground. Seamless matte sage-grey composite shell, dark charcoal band along the lower edge, one flush recessed door. A-frame tongue and ball coupler at the tall end. 35mm, shallow depth of field, architectural product photography.

## 4. Scene prompts (apply §1 geometry to each)

- **Hitched to the Model Y** — three-quarter rear, coastal highway, flat roofline below the car's roof, 7-pin cable + safety chain at the coupler, motion-blurred road, 50mm.
- **Camp mode** — forest campsite, unhitched on tongue jack, rigid roof raised ~20" on four slim posts with taut grey fabric walls glowing warm, rear hatch propped open (transverse bed + galley), orange cable running to a parked EV's charge port, blue hour.
- **V2H winter** — suburban driveway at dusk, snow, heavy black cable to a grey inlet box on the house wall, house windows warm while neighbours are dark, green status LED.
- **Aero study** — side profile, dark studio, cyan streamlines reattaching over the flat roof and converging at the squared tail, undisturbed flow beneath the enclosed running gear, CFD aesthetic.
- **Technical cutaway** — side elevation on white, dimension lines: pack slab in the floor (~7' × 5' × 6" + rear hump), aluminium frame around it, skid plate, donor rear subframe at ~54% of box length, bed platform over the hump.

---
*v0.1, 2026-07-24. Update the failure log every time a render goes wrong — that table is the actual asset.*
