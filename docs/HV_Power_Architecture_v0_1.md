# HV-First Power Architecture — v0.1 ("kill the 12V spine as a power bus")

**Date:** 2026-07-24 | **Trigger:** TJ: "2.4 kW at 12V is practically useless — massive wiring, huge losses, DC→12V→AC is wasteful. I want to pull from the HV pack directly. Have we covered that?"
**Status:** design memo — **changes locked decision D-F2** (Flagship Plan) if adopted. Configurator carries it as the `hv_hybrid` option.

## 1. Straight answer

**Partially covered before; not the way you want.** The prior design put the Solis at the HOUSE only; on the road the trailer ran everything through PCS→12V→MultiPlus→120VAC — exactly the double conversion you're objecting to, and you're right to object: ~80–85% round-path vs ~97% single-conversion, plus 200A-class 12V cabling.

**The fix is real and buildable today.** But one physics honesty first: a *pure*-DC trailer at 400V isn't — there is no 400VDC appliance ecosystem (induction hobs, toasters, water-heater elements are AC-input devices), and DC arcs weld switch contacts; every DC branch circuit would be HV electrician work. What IS buildable is your actual goal — **no double conversion, ever**:

## 2. Three-rail doctrine (replaces "12V spine")

| Rail | What lives on it | Conversion count |
|---|---|---|
| **400V DC bus** (the spine now) | Drive unit · **cabin cooling: Tesla S/X Gen2 A/C compressor run DIRECTLY at pack voltage** — openinverter has the CAN protocol fully documented (bytes 0–1 = duty cycle, 2–3 = max watts; wake = 12V pin 1) · **heat: salvage 400V EV coolant heater → hydronic loop** (shower water + space heat, one device) · dock/shore charging | **ZERO** — this is the all-DC answer where it actually works |
| **240/120 VAC** via ONE conversion: **Solis S6-EH1P11.4K-H-US mounted IN the trailer** (battery window 120–500V ✓ covers 355V LFP and ~360–400V nickel; 97.6% peak; UL9540; grid-forming EPS <10 ms) | Induction cooking · toaster/microwave · water heater element (if not hydronic) · **charging the CAR from the pack: EPS 240V → 32A EVSE → Y's onboard charger, up to ~7.6 kW** · V2H generator mode at ~10 kW class | ONE (~97%) |
| **12V control rail** (demoted, ~300–500W) | Lights, pumps, fans, sound, actuators, Cerbo, brake/breakaway (legally must exist anyway — 7-pin, breakaway battery) | PCS makes it for free; 25–40A wiring, not 200A |

**MultiPlus 12/3000 is DELETED.** The Maguire PCS stays (12V rail only). Solar goes **DC-coupled into the Solis MPPTs** (4 MPPTs, 600V max — wire the roof array ≥2 panels in series to clear MPPT start voltage; no more 12V MPPT + buffer-first path). **The donor PCS keeps its FULL role (TJ, 2026-07-24): 11 kW AC charging + 12V rail both stay.** The Solis AC-in is a *second, independent* charge path — two paths into the pack is redundancy, not waste, on a pioneer build. Only Elcon/Volt-stack chargers become redundant next to the Solis.

## 3. What the Solis is and isn't (your direct question)

Yes — Battery-Emulator + Solis on the HV pack feeds the trailer **as AC**, whole-trailer, one conversion. It is NOT a DC power supply: its only DC ports are battery and PV; hybrid inverters have no DC load outputs. "DC devices fed from the pack" = tap the 400V bus directly (fused HV branch + HVIL discipline, Guide #2 rules) for HV-native salvage hardware — compressor, coolant heater — not through the Solis.

## 4. Load-by-load (your list)

Cooling → HV-direct compressor (proven S/X Gen2 path; Model 3 supermanifold/Octovalve controller is an active openinverter project — watch it, don't wait for it). Shower/space heat → HV hydronic loop. Cooking, toaster → AC rail (induction). Lighting, sound, pumps → 12V control rail (they're inherently 12V devices; tiny wires at this power). Solar → Solis MPPT DC-coupled. Pack→car → 240V EVSE off EPS. Shore/dock → Solis AC-in.

## 5. V2H consequence (big)

With the inverter ON the trailer, **generator-mode V2H jumps from 2.4 kW to ~10 kW class** through a 50A inlet+interlock — the $500 house kit becomes the whole house-side story for backup duty. The house-side dock Solis drops to OPTIONAL (only for grid-interactive winter duty: TOU arbitrage/export need a permanent AHJ-blessed install; an interlock can't parallel the grid).

## 6. Honest caveats

1. Solis is a stationary residential unit: trailer mounting = vibration isolation + mobile use outside its listing (same pioneer gray zone as the rest of the build; EPS/off-grid mode when camping). Verify EPS continuous rating on the datasheet at order time (~9.6–11.4 kW class).
2. MPPT start voltage vs a small roof array — series-string the panels; confirm at panel selection.
3. Every HV branch = pyro/fuse + HVIL discipline (Guide #2). The 400V bus now leaves the pack bay: compressor + heater branches need the same rigor as the DU run.
4. This **revises locked D-F2** (was: 12V spine + MultiPlus). Weight ≈ wash (Solis ~57 lb vs MultiPlus ~42 + deleted 12V fat wiring); cost +$1.3K net on the trailer, −$2.4K if the house dock Solis is dropped → **net cheaper for more capability**. Flagship Plan changelog entry pending TJ's confirm.

*v0.1, 2026-07-24. Sources: Solis S6-EH1P datasheet (120–500V battery, 97.6%, UL9540, <10ms EPS), dalathegreat/Battery-Emulator (400V BYD emulation, Solis+Tesla confirmed in the field), openinverter wiki "Tesla Model S/X A/C Compressor Gen2" (CAN protocol documented), openinverter "Tesla Heatpump Controller" thread (Model 3 supermanifold, in progress).*
