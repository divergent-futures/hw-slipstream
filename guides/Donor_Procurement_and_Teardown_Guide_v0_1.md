# Donor Procurement & Teardown Guide — Salvage Tesla Model 3/Y

**v0.1 · 2026-07-08 · Slipstream open-source build series**
**What this is:** a follow-along procedure for buying a crashed Model 3/Y and harvesting its battery pack and drive unit for a Slipstream Range-Neutral build. Written for a careful first-timer with garage tools. Research basis: `docs/Slipstream_Salvage_V2H_Research_v0_1.md` + procurement research 2026-07 (all claims sourced in the research transcripts; Tesla's own service manuals are free at service.tesla.com and are the authority for every wrench step).

> **⚠️ READ FIRST — the three rules that keep you alive**
> 1. **The pack is always live.** 350–400 VDC exists inside the pack regardless of what the car thinks. Contactors open ≠ dead. Busbars ahead of the contactors are always energized.
> 2. **You never open the pack.** This whole architecture keeps the pack sealed — Tesla's BMS, contactors, pyro fuse, and cooling stay in charge. If your plan involves opening the lid, stop and re-read the architecture docs.
> 3. **One hand, gloves on, buddy nearby.** Class-0 (1,000V) insulated gloves with leather protectors for any HV connector work, one-hand rule, insulated tools, a second person within shouting distance who knows not to grab you.

---

## Phase 0 — Before you bid

**Know what you're buying.** Target: **Fremont-built (VIN digit 11 = "F"), 2170 Long Range** Model 3/Y (78 kWh, 96s46p, ~1,054–1,168 lb pack) or **2021+ RWD/SR with CATL LFP** (55–60 kWh, ~966 lb, safer chemistry, happy at 100% charge — arguably the better trailer/V2H pack). **Never an Austin-built ("A") 4680 structural pack** — foam-potted, integrates the seats, not harvestable as a unit you can work with.

**Equipment checklist (have it before the car arrives):**
- [ ] Class-0 HV gloves + leather protectors + glove inflation test (date-stamped, in-test)
- [ ] CAT III/IV multimeter rated ≥1000V, insulated tool set, safety glasses, face shield
- [ ] 12V jump pack / bench supply (donor's LV battery will be dead)
- [ ] Scan My Tesla app + OBD harness for your donor's year (pre-2019 vs 2019+) + OBDLink MX+ dongle (~$130 all-in)
- [ ] QuickJack/2-post lift or 4 rated jack stands at full height, plus a **motorcycle/ATV lift table rated ≥1,500 lb** (the pack comes DOWN, not out the side)
- [ ] Coolant catch pans (~3 gal capacity), G48 disposal plan
- [ ] Non-conductive pack cradle/pallet + outdoor storage spot away from structures
- [ ] Fire posture: ABC extinguisher (for incidentals — a pack in runaway is not extinguishable; your plan is *distance*), garden hose, clear egress

**Budget math.** Hammer $3–7K + auction fees (~10% + ~$100–160 bid fee + ~$95 gate + env/title ≈ **$800–1,300 on a $4K car**) + broker $200–600 if your state requires one + tow home. Sanity rule: if donor all-in exceeds ~60% of buying a tested pack ($5.5–10K) + drive unit ($3–6K) from a recycler (Calimotive, EV West, J&J), skip the gamble. Part-out resale (Phase 6) typically claws back $2–5K+.

## Phase 1 — Source and select

1. **Register:** Copart (Basic $99/yr) and/or IAAI (~$200/yr, photo ID). Check your state on IAAI's buyer-eligibility page — CA/CT/VA/MI/IL-class states need a broker ($200–600 flat) for salvage titles.
2. **Search & calibrate:** live inventory on both; **bid.cars** shows historical hammer prices — spend an evening there before bidding anything.
3. **Selection filter — bid only when ALL true:**
   - [ ] Damage geometry acceptable: **hail is the top-tier donor** (cosmetic write-off, pack/drivetrain/thermal all intact), **rear** preserves the front thermal gear, **front** is fine for pack-only harvest. **Side and undercarriage hits are inspect-first, not auto-reject** — extensive-looking damage can be shallow; go look (or buy contingent on the Phase-3 BMS gate) before striking them
   - [ ] **Year strategy — SPLIT-DONOR (corrected 2026-07-10, see `docs/Pack_Selection_Memo_v0_1.md`):** the pack and drive unit need not come from the same car. **PACK donor: 2022–2024 Model 3 "RWD" trim = CATL LFP Gen2 60 kWh — the newest LFP that exists in US salvage** (the US LFP window closed Oct 2024 on tariffs; 2025+ US Teslas are all nickel chemistry; the same Gen2 pack design still ships new in Canada in 2026, so this is current technology, not old). Identify by trim "RWD"/"SR" — never "Long Range"/"Performance." Plan-B pack: Ford Mach-E Standard Range 2023+ (CATL LFP ~72 kWh, better Battery-Emulator support — but no Tesla PCS, so the 12V spine falls back to Elcon + 400→12V DC-DC). NCA fallback: any LR 2170 pack, abundant, with 60–80% SoC parking discipline. **DRIVE UNIT: from the proven 2021–2023 pool** (recycler unit $1–2K, or a second cheap donor) — open logic boards are demonstrated pre-Highland only. Lockdown reality: Tesla VIN-locks parts *ordering* and gateway pairing, but nothing blocks standalone pack operation — the open stack replaces Tesla firmware entirely
   - [ ] **"Run and Drive"** flag if available (weak promise, but it's the best cheap signal the pack was alive post-crash)
   - [ ] VIN digit 11 = **F** (Fremont); trim confirms 2170 LR or CATL LFP
   - [ ] Title = salvage certificate (keeps hulk resale open) — parts-only/non-repairable is acceptable *and cheaper* if your state lets you buy it and you'll scrap the shell
4. **Hard NOs — walk away:**
   - ✕ **Flood/water damage, any hint** (damage code, water lines, silt, fogged lenses, coastal hurricane yards). Flood packs corrode internally and can go into *delayed* thermal runaway. Not negotiable.
   - ✕ Fire damage, melted underbody plastics
   - ✕ ~~Hard side impact or underbody strike~~ → moved to inspect-first (above): photos can't clear them, but eyes-on + the Phase-3 BMS gate can. The pack enclosure inspection in Phase 3 is the real gate
   - ✕ Dash photos showing **BMS_u029 / BMS_u018** ("maximum charge level reduced" / brick imbalance) — that car is at auction *because* the pack is dying
   - ✕ Austin 4680 structural pack
5. **Airbags deployed is FINE.** Deployment fires the pyrotechnic HV disconnect — that's a ~$100–300 replaceable part, and it's why the listing says the HV is dead. The modules behind it are usually untouched. This is the single biggest mispricing in the market and it works in your favor.

## Phase 2 — Buy and transport

1. Bid your number, not the adrenaline number (fees add ~25–30% on cheap lots).
2. **Transport the WHOLE CAR — do not extract at the yard.** A lithium pack installed in a vehicle is excepted from the UN3480/Class-9 bare-battery shipping rules; a bare 480 kg pack is regulated hazmat freight (ground-only if suspect, marked packaging, hazmat-papers territory). Tow-truck or U-Haul auto transport the hulk to your workspace and the problem disappears.
3. At drop-off: park it outdoors, away from structures, on a non-combustible surface. It stays there until Phase 3 clears it.

## Phase 3 — Wake it and verify (the go/no-go gate)

1. **Inspect before energizing:** crawl the underbody (creeper + light). Look for pack enclosure deformation, punctures, coolant weep, crash damage reaching the rocker/pack flange, damaged orange HV cabling. Any enclosure breach → **STOP**: the pack is DDR-class; your options are recycler pickup, not reuse.
2. **Revive LV:** connect the 12V/16V jump supply per the service manual access point. Car electronics wake; the HV may stay down (fired pyro) — that's expected.
3. **Read the BMS:** Scan My Tesla via the diagnostic connector (behind the console — the "OBD port" carries no data), or Service Mode battery health screen. Record:
   - [ ] **Nominal Full Pack** (kWh) → SoH = NFP ÷ new-spec (78 LR / 55–60 LFP). **Gate: ≥80% SoH** for the flagship build; 70–80% = negotiable for V2H-heavy duty; <70% = part it out
   - [ ] **Cell voltage spread** — min-to-max **>100 mV = bad brick → STOP**, that pack is a donor of parts, not a heart
   - [ ] Stored BMS alerts — u029/u018 present → same verdict
   - [ ] Isolation resistance reading if available
4. Pyro fired? Note it; the replacement (EV West/Gruber, $100–300) gets installed during commissioning — **never bridge it with a solid bar**; it's the pack's main overcurrent protection.

## Phase 4 — Extraction (follow the Tesla manual, in this order)

Tesla's service manual procedures (free, service.tesla.com: "HV Battery — Remove & Replace" for your exact model/year/drivetrain) are the wrench-by-wrench authority. The shape of the job:

1. **Safety gate — electrical isolation.** 🧤 Gloves on for everything from here involving orange cable or the penthouse:
   - [ ] Disconnect LV power per manual; pull the first-responder loop (disconnect, never cut)
   - [ ] Wait ≥2 minutes for discharge
   - [ ] **Verify dead: <10 VDC at the HV connector points the manual specifies.** Reading >10V means welded/closed contactors — **STOP, do not proceed**; that pack needs professional handling
2. **Coolant.** Drain at the pack quick-connects into catch pans (~2–3 gal G48). Have towels; it will not be graceful. Dispose per local rules (it's ethylene glycol — animals are attracted to it and it kills them; contain everything).
3. **Interior bolts.** Rear seat and carpet come up — the pack bolts through the cabin floor. Left and right rear interior fasteners per manual.
4. **Disconnections at the penthouse:** HV harness, charge-port harness, comms/LV connectors, coolant lines. 🧤 Gloves + one-hand for the HV connector. Cap/bag every connector — penthouse output lugs are **always at pack potential**; fit the manual-specified covers immediately.
5. **The drop.** Car high on lift/stands (you need ~4+ ft under it to roll the loaded table out). Lift table centered under the pack, ~30 perimeter + interior fasteners out (count varies by year/drivetrain — the manual lists every one), lower in stages, checking snags at each inch. **1,050–1,170 lb.** Nobody's hands go under it, ever. Two people minimum for the roll-out.
6. **Immediately:** onto the non-conductive cradle, terminal covers on, HVIL connectors bagged and labeled, photograph everything (your future commissioning self will thank you).

## Phase 5 — Storage and care

- Outdoors or detached structure, off direct sun, non-combustible surface, away from anything you love
- Target **~30–50% SoC** for storage (lower stored energy = lower consequence; the BMS keeps itself alive on minimal draw — check monthly via the LV connector + Battery-Emulator or SMT)
- Winter: the pack tolerates cold storage fine; **never charge below 0°C** (the BMS enforces this — don't defeat it)
- Keep the HVIL loop intact and documented — the commissioning step (Battery-Emulator, SS08) depends on it

## Phase 6 — Harvest the rest, then sell the bones

**Take (in rough order of value to the build):**
- [ ] **Rear drive unit WITH subframe + suspension** (unbolts as an assembly — the standard "drop-in" harvest; also the highest-resale item if you go front-SDU instead)
- [ ] **Charge port + charge-port ECU + port-to-pack HV harness** (required for PCS charging; Gen4 ECU enables CCS)
- [ ] Drive-unit harness (spliceable; labeled aftermarket versions exist)
- [ ] Coolant pumps + lines feeding the pack (pack thermal in the trailer)
- [ ] **THE COMPLETE THERMAL SYSTEM (Lane-2 harvest, costs nothing extra):** Octovalve/SUPERMANifold, HV AC compressor, radiators + chiller, cabin HVAC assembly, every thermal harness. No CAN on the manifold — it needs the (WIP) open-source heat pump controller to run outside the car, but harvested now it's a free future upgrade that unifies cabin climate + pack thermal + DU cooling off the HV pack. **Donor nuance: this gear lives in the FRONT of the car — rear-hit donors preserve both the pack and the thermal system; front-hit donors may have crushed it.**
- [ ] LV harness sections, mounting hardware, and every orange cable run

**Sell (typical part-out yields):** MCU/screen $1,200–2,500 · wheels/tires ~$2K · doors, glass, lights, seats, door handles ($200–300 each!) · unused drive unit $3–6K. Parting out yields 30–40% over selling whole; budget 2–3 hours per item to pull/test/list. Salvage-cert shell → rolling shell to rebuilders; parts-only shell → scrap.

---

## STOP conditions (the whole list, one place)

| Condition | Verdict |
|---|---|
| Flood history, any evidence | Never bid / never energize |
| Pack enclosure breach, puncture, coolant weep | Recycler pickup — not reuse |
| >10 VDC at HV terminals after isolation steps | Professional handling only |
| Cell spread >100 mV, BMS_u029/u018, SoH <70% | Pack = parts, not a heart |
| Any impulse to open the pack lid | Re-read the architecture. The pack stays sealed. |
| Working alone on HV steps | Wait for your buddy. It keeps. |

## What comes next

Pack on the cradle + drive unit on the bench → **SS08 commissioning**: Battery-Emulator on the LV connector, first CAN conversation, contactor close, and the pack's second life begins. Drive unit → SS07 (Maguire M3-DU board or EV Controls T2-C). House-side V2H kit → SS08 Tier 1.

*v0.1 — first-timer review wanted: if you follow this and find a gap, file an issue. Safety sections reviewed against Tesla service manual procedures, PHMSA lithium guidance, and NHTSA flood-EV teardown findings; this guide is information, not certification — you are responsible for your own competence with high-voltage systems.*
