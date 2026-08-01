#!/usr/bin/env python3
"""flagship_mass_budget.py — component-level mass inventory for the Slipstream flagship.

Doctrine: the mass model lives in code (same rule as flagship_balance.py).
Every number is a pre-scale ESTIMATE, superseded by the first real weighing.
Run: python3 flagship_mass_budget.py    (prints the tables that seed SS05b)
"""

# (id, category, lb, note, strip: None or (tier, savings_lb, what_it_costs))
ITEMS = [
    # --- structure ---
    ("frame_belly_skid",   "structure", 300, "12' frame + belly fairing + skid (SS05)", None),
    ("shell_popup",        "structure", 380, "composite shell + pop-up, 1\" walls (SS04)", None),
    # --- drive / running gear ---
    ("du_subframe",        "drive", 480, "rear DU + subframe + suspension + brakes + halfshafts (SS05a: donor assembly IS the axle)", None),
    ("wheels_tires",       "drive", 120, "donor 18\" pair", ("S1", 24, "aftermarket flow-formed 18\" pair (~48 lb/pair vs ~72)")),
    ("eh_brake_actuator",  "drive", 12,  "electric-over-hydraulic actuator", None),
    ("hitch_coupler",      "drive", 45,  "coupler + load-cell insert + tongue hardware", None),
    ("tongue_jack",        "drive", 18,  "jack + caster", ("S1", 6, "aluminum jack")),
    # --- energy ---
    ("pack",               "energy", 966, "LFP 966 / NICKEL 1,054 (+88) — first good donor wins", None),
    ("buffer_12v",         "energy", 28,  "100Ah 12V LFP buffer", None),
    ("solis_mounted",      "energy", 66,  "Solis S6 11.4K (58) + isolation mount plate (8)", None),
    ("hv_wiring",          "energy", 40,  "HV runs: DU, compressor, heater branch, EVSE + inlet", None),
    ("lv_wiring",          "energy", 25,  "12V control rail (25-40A class, no 200A fat runs)", None),
    # --- car-brain harvest (SS09) ---
    ("car_computer_screen","carbrain", 15, "Car Computer + touchscreen", None),
    ("body_controllers",   "carbrain", 8,  "VCFRONT + VCLEFT + VCRIGHT", None),
    ("vcsec_antennas",     "carbrain", 2,  "VCSEC + NFC/BLE antennas", None),
    ("harness",            "carbrain", 25, "donor harness sections (copper!)", ("S1", 10, "trim to length, strip unused branches at bench")),
    ("supermanifold",      "carbrain", 30, "supermanifold + Octovalve + chiller", None),
    ("compressor",         "carbrain", 20, "HV compressor", None),
    ("hvac_box",           "carbrain", 35, "cabin HVAC box (blower/evap/cabin condenser/doors)", ("S3", 20, "custom air handler w/ donor core — HURTS native Camp mode; last resort")),
    ("radiator_fans",      "carbrain", 22, "radiator + fan + shroud", None),
    ("coolant_pumps",      "carbrain", 6,  "2x coolant pumps", None),
    ("charge_port",        "carbrain", 8,  "NACS charge port assembly + ECU", None),
    ("lv_aux_batt",        "carbrain", 5,  "donor lithium aux battery", None),
    ("cameras",            "carbrain", 2,  "rear + 2 repeaters", None),
    # --- fluids (aboard whenever operational) ---
    ("coolant_ext",        "fluids", 25, "coolant in external loops (pack-internal coolant counted in pack)", None),
    ("refrigerant",        "fluids", 3,  "R1234yf charge", None),
    ("brake_fluid",        "fluids", 2,  "E/H actuator + donor calipers", None),
    # --- water & plumbing (DRY) ---
    ("fresh_tank",         "water", 20, "20 gal tank, empty", ("S2", 5, "15 gal tank (also -42 lb payload when full)")),
    ("gray_tank",          "water", 12, "10 gal tank, empty", None),
    ("pump_lines",         "water", 12, "pump + PEX + valves", None),
    ("water_heater",       "water", 25, "120V 6-gal tank style", ("S1", 25, "DELETE: hydronic loop off the 400V coolant heater does shower + space heat (HV memo)")),
    ("composting_head",    "water", 28, "composting toilet", ("S2", 6, "lighter urine-divert dry toilet")),
    ("shower_kit",         "water", 8,  "outdoor shower fixture + curtain", None),
    # --- interior ---
    ("bed",                "interior", 70, "platform + mattress", ("S1", 15, "lightweight foam + slat platform")),
    ("galley_fridge",      "interior", 120, "counter, sink, induction, 12V fridge", ("S1", 6, "portable induction instead of built-in")),
    ("cabinetry",          "interior", 60, "cabinetry + fixtures", ("S1", 20, "CNC-lightened panels, foam-core doors (foamie tech upstream!)")),
    ("floor_finish",       "interior", 30, "floor + interior finish", None),
    # --- systems ---
    ("solar",              "systems", 70, "800W rigid panels + mounts", ("S1", 40, "semi-rigid lightweight panels + bonded rails (~30 lb total)")),
    ("starlink",           "systems", 3,  "Starlink Mini + mount", None),
    ("popup_actuators",    "systems", 30, "4x PA-17 actuators", ("S2", 22, "manual lift + gas struts — loses one-button pop-up")),
    ("fans_vents",         "systems", 10, "Maxxair + vents", None),
    ("sound",              "systems", 8,  "speakers/amp", ("S1", 6, "portable BT speaker rides as payload instead")),
    ("electronics",        "systems", 6,  "modeswitch + BE nodes + enclosures", None),
    ("breakaway_7pin",     "systems", 5,  "breakaway kit + 7-pin harness", None),
    ("stabilizer_jacks",   "systems", 40, "4x corner stabilizer/leveling jacks - CAUGHT BY RENDER 2026-08-01 (camp-mode image showed them; they were missing from the budget entirely)", ("S2", 12, "scissor jacks -> lighter drop-down or stack-block leveling")),
]

NICKEL_DELTA = 88
PAYLOAD_GEAR = 310          # gear + food + misc, weekend discipline
WATER_FULL   = 167 + 0      # 20 gal fresh @ 8.34 lb/gal; gray assumed EMPTY when towing (dump rule)
CAP = 3500

def total(items=ITEMS, skip=()):
    return sum(lb for i, c, lb, n, s in items if i not in skip)

def savings(tiers):
    return [(i, s[1], s[2]) for i, c, lb, n, s in ITEMS if s and s[0] in tiers]

if __name__ == "__main__":
    cats = {}
    for i, c, lb, n, s in ITEMS: cats[c] = cats.get(c, 0) + lb
    print("=== category roll-up (LFP pack baseline) ===")
    for c, lb in cats.items(): print(f"  {c:10s} {lb:5d} lb")
    dry_lfp = total(); dry_ni = dry_lfp + NICKEL_DELTA
    print(f"\nDRY: LFP {dry_lfp} | nickel {dry_ni}")
    for name, dry in (("LFP", dry_lfp), ("nickel", dry_ni)):
        tow_full  = dry + PAYLOAD_GEAR + WATER_FULL
        tow_empty = dry + PAYLOAD_GEAR
        print(f"{name}: tow w/ full fresh {tow_full} ({tow_full-CAP:+d} vs cap) | tow water-empty {tow_empty} ({tow_empty-CAP:+d})")
    s1 = savings({"S1"}); s1_total = sum(x[1] for x in s1)
    s2 = savings({"S2"}); s2_total = sum(x[1] for x in s2)
    print(f"\nS1 (no capability loss): -{s1_total} lb")
    for i, lb, note in s1: print(f"  -{lb:3d}  {i}: {note}")
    print(f"S2 (capability trades): -{s2_total} lb")
    for i, lb, note in s2: print(f"  -{lb:3d}  {i}: {note}")
    print("\n=== war status after S1 ===")
    for name, dry in (("LFP", dry_lfp), ("nickel", dry_ni)):
        d = dry - s1_total
        print(f"{name}+S1: dry {d} | tow water-empty {d+PAYLOAD_GEAR} ({d+PAYLOAD_GEAR-CAP:+d}) | tow full-fresh {d+PAYLOAD_GEAR+WATER_FULL} ({d+PAYLOAD_GEAR+WATER_FULL-CAP:+d})")


# ---------------- V1 staged-build scenarios (TJ, 2026-07-24) ----------------
# V1 = nickel pack + wheels, NO truck drive, NO car-brain/cooling loop (passive
# pack: 11 kW charge = 0.14C on 78 kWh - benign; verify at commissioning).
# V2 = the designed-in upgrade: DU + car-brain + full cooling loop.

V1_REMOVE = {"du_subframe", "car_computer_screen", "body_controllers", "vcsec_antennas",
             "harness", "supermanifold", "compressor", "hvac_box", "radiator_fans",
             "coolant_pumps", "lv_aux_batt", "cameras", "coolant_ext", "refrigerant"}
# keep: charge_port (inlet hw for Maguire-PCS charging), eh_brake_actuator (donor calipers)

V1_ADD_SUBFRAME = [("subframe_no_du", 300, "donor rear subframe, DU removed (DU develops on the bench; bolts in for V2)"),
                   ("tankless_120v", 8, "120V tankless water heater (no hydronic loop in V1)"),
                   ("hv_wiring_credit", -12, "no DU/compressor HV branches yet")]
V1_ADD_TIMBREN  = [("timbren_axle", 130, "Timbren axle-less pair + hubs + electric brakes"),
                   ("tankless_120v", 8, "120V tankless water heater"),
                   ("hv_wiring_credit", -12, "no DU/compressor HV branches yet")]
S1_V1 = 152 - 25   # water-heater delete n/a in V1 (tankless replaces hydronic)

def v1_dry(adds, nickel=True):
    d = total(skip=V1_REMOVE) + sum(lb for _, lb, _ in adds)
    return d + (NICKEL_DELTA if nickel else 0)

if __name__ == "__main__" and True:
    print("\n=== V1 staged-build (nickel) ===")
    for name, adds in (("subframe-no-DU route", V1_ADD_SUBFRAME), ("Timbren route", V1_ADD_TIMBREN)):
        d = v1_dry(adds)
        for label, dd in ((f"V1 {name}", d), (f"V1 {name} + S1", d - S1_V1)):
            print(f"{label}: dry {dd} | tow water-empty {dd+PAYLOAD_GEAR} ({dd+PAYLOAD_GEAR-CAP:+d}) | tow full-fresh {dd+PAYLOAD_GEAR+WATER_FULL} ({dd+PAYLOAD_GEAR+WATER_FULL-CAP:+d})")
    up = 180 + 170 + 28 + 12 - 8   # DU + car-brain + fluids + HV branches - tankless
    print(f"\nV2 upgrade adds back ~{up} lb -> full flagship (the war already closed in §3)")


# ---------------- unified branch matrix (TJ, 2026-07-24) ----------------
GRAY_FULL = 83   # 10 gal gray @ 8.34 - camp-only mass (dumped before ANY towing)

def matrix():
    S1_FULL = sum(s[1] for i,c,lb,n,s in ITEMS if s and s[0]=="S1")
    rows = []
    v2 = total()   # full flagship = the complete inventory
    for branch, dry_lfp, s1 in (("V1 energy trailer", v1_dry(V1_ADD_SUBFRAME, nickel=False), S1_V1),
                                ("V2 full flagship", v2, S1_FULL)):
        for chem, delta in (("LFP", 0), ("nickel", NICKEL_DELTA)):
            for strip, sdel in (("base", 0), ("+S1", s1)):
                d = dry_lfp + delta - sdel
                rows.append((f"{branch} {chem} {strip}", d,
                             d+PAYLOAD_GEAR, d+PAYLOAD_GEAR+WATER_FULL,
                             d+PAYLOAD_GEAR+WATER_FULL+GRAY_FULL))
    return rows

if __name__ == "__main__" and True:
    print("\n=== BRANCH MATRIX (tow cols vs 3,500 cap; camp static has no cap - GAWR check instead) ===")
    print(f"{'scenario':34s} {'dry':>5s} {'tow-empty':>10s} {'tow-full':>9s} {'camp-static':>11s}")
    for name, d, te, tf, cs in matrix():
        flag = lambda w: f"{w}({w-CAP:+d})"
        print(f"{name:34s} {d:5d} {flag(te):>10s} {flag(tf):>9s} {cs:>11d}")
