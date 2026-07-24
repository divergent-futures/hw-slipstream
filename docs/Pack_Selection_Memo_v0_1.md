# Flagship Pack Selection Memo — v0.3

**Date:** 2026-07-10 | **Trigger:** TJ's challenge to the pack assumption ("no US LFP post-IRA; Canadian Shanghai LFP; is Tesla still right?") | **Research:** 16-search verified pass, sources in transcript
**Supersedes:** the "2024–2025 pack donor preferred" line in the split-donor strategy — that window is nearly empty for LFP.

## 1. The chemistry map (verified)

| Year / market | Model 3 RWD/Standard | Model 3/Y LR/Perf | Model Y RWD/Std US |
|---|---|---|---|
| 2021 (late)–2023 US | **CATL LFP** (Gen1 55 → Gen2 60 kWh) — base trim, ~2.5 yrs of volume | 2170 NCA ~78 kWh | 2170 NCA / Austin 4680 |
| 2024 US (Highland) | **CATL LFP** — thin slice (lost IRA credit Jan '24, discontinued Oct '24 on tariffs) | 2170 (LG NMC / Panasonic NCA) | 4680 / 2170 |
| 2025–26 US | **No LFP exists.** "Standard" trims = 2170 NCA/NMC ~69.5 kWh | 2170 | 2170 (4680 wound down) |
| 2022–Aug 2024 Canada | **Shanghai-built CATL LFP** | — | — |
| Late 2024–early 2026 Canada | Fremont nickel cars (100% China tariff) | — | — |
| May 2026+ Canada | **Shanghai LFP returns** (tariff deal, C$39,490) — salvage volume in 1–2 yrs | — | — |

**The reframe that answers "I don't want 3-year-old tech":** the Gen2 CATL 60 kWh pack in a 2022–23 US car is the *same pack design* Tesla resumed selling new in Canada in May 2026. US LFP isn't old technology — it's current technology whose US sales window closed for tariff reasons, not engineering ones. LFP's minimal calendar aging plus our ≥80% SoH commissioning gate means a 2023 pack that passes is functionally current. Meanwhile "newest" (2025–26) means nickel chemistry — newer calendar, older safety posture.

## 2. The ranking

1. **✅ PRIMARY: US-salvage 2022–2024 Model 3 RWD — CATL LFP Gen2 ~60 kWh.** Base-trim volume for 2.5 years = routinely at US auctions (identify by trim "RWD," never "Long Range/Performance"). ~355V-class, penthouse PCS intact (the 12V spine lives), Battery-Emulator supported (⭐ — pair with their Discord; LFP quirks documented in issues #1319/#1225), donor $5–8K with part-out offset. 60 kWh vs the plan's 55–60 assumption: unchanged.
2. **🥈 Ford Mustang Mach-E Standard Range 2023+ — CATL LFP, ~72 kWh usable, 347.8V, 108s, non-structural.** More energy than Tesla LFP and Battery-Emulator rates it ⭐⭐ (better than Tesla). **Architectural cost:** no Tesla PCS → the 12V house spine falls back to Elcon + industrial 400→12V DC-DC (+~$2.5K, risk #7's fallback becomes baseline). Fewer at salvage. Take one if it appears cheap and clean; confirm LFP-variant emulator support on their Discord first.
3. **🥉 US-salvage Model 3/Y LR 2170 NCA ~75–82 kWh — the abundance fallback.** Most available donor, biggest capacity, mature DIY-storage precedent with intact sealed packs. Discipline required: park/dock at 60–80% SoC (NCA calendar-ages fast at 100%; LFP doesn't) — costs V2H headroom, not safety per se; fire margin is genuinely lower than LFP. Choose if timeline beats chemistry.
4. **Canada import — documented fallback, not the play.** IAA Canada allows public registration; the clean route is the HS-7 "assemblage" parts import (drivetrain out) or bare-pack UN3480 ground freight — but budget broker + hazmat carrier + likely **25% Section-301 duty on a Chinese-origin pack**, for hardware US yards already stock. Revisit only if US LFP supply proves thinner than it looks, or in ~2028 when May-2026 Shanghai cars reach Canadian salvage.
5. **❌ Avoid:** Austin 4680 structural (unchanged), 2025–26 Standard trims as *pack* donors (nickel + too new for salvage; fine as DU/subframe donors later).

## 3. What changed in the project (this commit)

- **donor-watch filter + daily briefing: Track 1 = 2022–2024 Model 3 RWD** (was 2024–2025 — a near-empty set for LFP). 2025+ lots now tagged honestly as nickel-chemistry LR-class.
- Guide #1 Phase 0/1 updated to the corrected window and the trim-identification rule.
- Flagship Plan D-F4 annotation: LFP target = Gen2 CATL 60 kWh, 2022–2024 donor; NCA fallback carries the 60–80% SoC discipline note.
- Mach-E documented as pack plan-B with the PCS/12V-spine consequence attached.

## 3b. Policy update (TJ, 2026-07-10 — v0.2): FIRST GOOD DONOR WINS

TJ's follow-up settled the real question: nickel is **acceptable**, and US ubiquity + proximity + newer cells are worth real money. Canada is out (shipping + duty + hassle for a chemistry advantage that doesn't justify it). So chemistry becomes a **tiebreaker, not a gate**:

- **[TRACK 1 LFP]** 2022–2024 Model 3 RWD — wins ties: wider thermal margin, 100% SoC dock tolerance (full 60 kWh available all winter), ~90–200 lb lighter in the 3,500 lb war
- **[TRACK 1B NICKEL]** 2023–2025 Model 3/Y LR / 2025 Standard — co-primary: +15–20 kWh, newest cells, best availability; costs +88–200 lb payload (tongue stays legal: recomputed ~310/334 lb) and **60–80% SoC dock discipline** (nickel calendar-ages fast at 100%; effective winter house storage ~48–64 kWh of an 80 kWh pack — the capacity edge partly evaporates in V2H duty). Slightly better cold behavior — worth something in CT.
- Buy whichever clean hail/rear donor appears first at the right price; LFP breaks same-week ties. The watch hunts both as equals; the architecture (Battery-Emulator, PCS, 12V spine, Digital HVIL for 2024+) is chemistry-agnostic and confirmed for all of them.

## 3c. Decision (TJ, 2026-07-24 — v0.3): NICKEL NOW; LFP/sodium stay in the configurator as the future

TJ called it: **go with nickel chemistry now.** LFP and (down the track) sodium-ion remain in the configurator deliberately — it extrapolates forward, and **V2H is the next most important metric**: a parked trailer is a ~70 kWh pack doing nothing, and it should replace a Powerwall, not sit idle.

**Bidirectional draw with the CURRENT architecture (the numbers):**

| Path | Power | Energy per day / event |
|---|---|---|
| **Tier 1 — generator mode** (inlet + interlock, any config) | ~2.4 kW cont. (MultiPlus 12/3000 through the 2.5 kW PCS 12V spine) | power-limited: ≤ ~48 kWh/day at full tilt; essentials-backup class |
| **Tier 2 — seasonal dock** (Solis 11.4 kW hybrid, Battery-Emulator HV direct) | ~10 kW class — Powerwall-3 power | chemistry-limited, below |
| Nickel ~78 kWh, daily band 70→30% | — | **~31 kWh/day** (TJ's 20–25 estimate was conservative-right); 60→40% = ~16; occasional deep outage cycle 100→10% = ~70 kWh |
| LFP 60 kWh, near-full band 90→10% | — | **~48 kWh/day** — out-dispatches the bigger nickel pack in home duty |
| Sodium (future), full band + any-SoC storage | — | ~54 kWh/day of a 60 kWh pack; cold-immune; the endgame V2H chemistry |

The nickel degradation logic TJ stated is correct and now embedded in the configurator: shallow **mid-SoC cycling (30–70%) barely ages nickel — it's sitting at 100% that does.** Daily V2H in that band is a *gentle* duty cycle, and even the 40% band beats a Powerwall 3 (13.5 kWh) by 2.3×. Configurator changes: `v2h` metric (kWh/day) on every config, sodium_future option + roadmap warn rule, chemistry notes rewritten on both Tesla pack options.

## 4. Standing honesty

No lithium pack is "safe" — LFP buys a wider thermal-runaway margin and no oxygen-releasing cathode, not immunity. The architecture's real safety layers are unchanged and chemistry-independent: sealed pack, Tesla BMS retained, intact pyro/contactors/HVIL, outdoor mounting, skid protection, and the Phase-3 inspection gates. Chemistry choice adjusts the margin; the discipline does the protecting.
