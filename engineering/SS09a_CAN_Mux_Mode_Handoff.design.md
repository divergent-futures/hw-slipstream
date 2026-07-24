# SS09a — Pack-Master Mode Handoff (the CAN mux) · Design Track

**Status:** v0.1 concept design | **Parent:** SS09 §3 | **Feeds:** Gate A bench criteria, Guide #2 (pack), Guide #4 (followdrive), SS07
**The problem in one line:** the pack's BMS can only serve one master at a time, and this build has two — the donor car-brain (cabin life) and the open stack (Battery-Emulator + Solis + ZombieVerter). Nobody has published a clean switchover. This is Slipstream's keystone contribution.

## 1. The three modes (not two — drive is the one everyone forgets)

| Mode | Pack master | What's running | Why this master |
|---|---|---|---|
| **CAMP** | **Car-brain** (gateway/VCFRONT/BMS native) | HVAC + Octovalve, Camp/Dog mode, screen/Theater, native NACS charging, app | The whole point of SS09 — Tesla software does cabin life better than we ever will |
| **DRIVE** | **Open stack** (Battery-Emulator + ZombieVerter/followdrive) | DU assist, regen, hitch-force loop | A "parked" car-brain watching 20–50 kW flow would be off-map behavior; the followdrive safety contract (Guide #4: any ambiguity = zero torque) requires OUR fault handling, not Tesla's |
| **STORE / DOCK** | **Open stack** (Battery-Emulator → Solis) | Winter V2H, solar charging, TOU dispatch | Field-proven BE+Solis path; car-brain fully powered down = zero vampire |

Drive-mode pack cooling rides SS07 Lane-2 provisions (open pump control + temp-derated assist via BE limits) — the car-brain is asleep on the road.

### 1b. The cooling conflict, resolved (TJ, 2026-07-24: "who cools the pack while OUR brain drives?")

The muscles are shared; only the brain switches. Pumps, radiator fan, compressor, and the Octovalve are dumb actuators — they obey whoever commands them, and none of them care which mode we're in. Three cooling levels:

- **Level 1 (DRIVE default): pumps + radiator + fan.** Simple 12V/PWM devices our supervisor runs directly. The heat math says this is nearly always enough: ~30 kW assist ≈ 0.6–0.9 kW pack heat (0.4C on a 60–78 kWh pack — gentle) + ~1.8 kW DU heat = **~2.5–3 kW total against a car-sized radiator with 50 mph of free airflow.** The EV-swap world runs Tesla DUs on pump+radiator alone as standard practice; cars only invoke the chiller for fast-charging and hot-day extremes.
- **Level 2 (DRIVE, hot day): + compressor→chiller.** The compressor takes simple documented CAN commands (duty % + max watts) — our side can run it without the car-brain if Level 1 falls short. Provisioned, not required.
- **Level 3 (CAMP): full Octovalve orchestration** — Tesla software, cabin + pack together. The DU is idle while camped, so there's no "Tesla must also cool the drivetrain" conflict: in CAMP the drivetrain makes no heat; in DRIVE the cabin needs none.

**The valve position is the one real coordination point:** the CAMP→DRIVE handoff sequence includes "leave the Octovalve in the drive/series position" before the car-brain powers down (or the supervisor nudges the stepper itself — bench question #5). Backstop regardless of all of it: BE reads pack temps from the BMS continuously, and followdrive derates to zero assist on over-temp — worst case the flagship becomes an ordinary dumb trailer mid-trip and the Y just tows it.

## 2. Architecture: switch the BUS, gate the BRAIN

Two physical actions, one mode selector:

1. **CAN mux** — a break-before-make DPDT signal-relay pair switches the pack CAN (X098 pins 16/15) between Branch A (donor car harness → gateway) and Branch B (open stack: BE + Maguire PCS controller + ZombieVerter). Mux mounts at the pack connector (stub < 30 cm). Each branch carries its own far-end 120Ω termination; the pack side keeps its own. The unselected branch floats dead — no partial connections ever.
2. **LV power gate** — the same selector gates 12V to the ENTIRE car-ECU set (VCFRONT chain, car computer, VCSEC). In DRIVE/STORE the car-brain is not asleep — it is OFF. A sleeping brain that wakes to find its battery amputated spams faults and drains 12V; a dead brain does neither. CAMP entry = power up, ~30–60 s boot, it finds its pack exactly where it left it.

**Never switched, ever:** HVIL (hardware loop stays continuous through all modes — the mux touches signal CAN only), pack 12V keep-alive (pins 8/18, fed from the 12V control rail permanently), pyro/contactor wiring.

## 3. The handoff sequence (always through SAFE)

Every transition passes through a verified dead state — no exceptions, including "quick" ones:

```
current mode → QUIESCE master        (car: end Camp, allow shutdown | BE: close session,
                                      command contactors open)
            → VERIFY SAFE            (contactors open confirmed: HV bus voltage decayed
                                      below 50V, measured independently by the supervisor)
            → GATE OFF old master LV (car-brain powers down / BE branch idles)
            → FLIP MUX               (break-before-make, both branches dead at flip)
            → GATE ON new master     → new master wakes pack per its own protocol
```

**Supervisor:** one ESP32 ("modeswitch") owns the sequence. Inputs: 3-position selector (CAMP / DRIVE / STORE), HV-bus voltage sense (isolated divider), 7-pin presence, BE heartbeat, car-awake sense (Branch A CAN activity). Refusal rules: no transition while HV bus is live; DRIVE requires 7-pin present (same permissive as followdrive); CAMP requires not-in-motion. State broadcast on the trailer's own CAN; manual override = documented lockout procedure, not a hidden jumper.

## 4. Interactions that make or break it (bench questions, Gate A)

1. **BMS wake choreography per master** — does the BMS state machine come up identically for the car vs BE after a master swap? Characterize on the bench FIRST; this is the highest-risk unknown and it costs $0 to test before the trailer exists.
2. **Car fault memory** — does the car log/latch anything from being power-cycled daily? (Expected: no — it's a normal 12V disconnect from its perspective.)
3. **Charge-session collision** — NACS charging (CAMP) and Solis dispatch (STORE) can never overlap by construction (different modes), but the supervisor must refuse mode change mid-charge: add "charge current = 0" to the SAFE check.
4. **Highland digital HVIL** — verify the HVIL-untouched claim holds on 2024+ packs (BE handles digital HVIL; confirm the car side tolerates our loop wiring).

## 5. BOM (bench build, Phase A)

ESP32 supervisor ~$10 · 2× automotive DPDT signal relays (or 1× 4PDT) + socket ~$30 · isolated HV voltage-sense module ~$40 · 3-position keyed rotary selector ~$25 · enclosure/connectors/loom ~$50 → **~$150–175 total.** It is deliberately dumb hardware — the invention is the *sequence*, and the sequence is what gets open-sourced (firmware + state diagram + bench log).

## 6. Safety doctrine (inherits Guide #2 + #4)

Single-master invariant enforced by PHYSICS (relay contacts), not software promises. HVIL integrity is mode-independent. Every transition transits verified-dead. Fail-anywhere = stay in current mode and alarm; the trailer never gets stuck half-switched because break-before-make + LV gating means the worst failure is "nothing is master" — which is just STORE-adjacent safe idle. The 12V control rail (buffer battery) keeps lights/supervisor alive through any handoff.

## 7. Open items

1. Bench characterization of BMS wake per master (Gate A add-on — the gating unknown)
2. Supervisor firmware (state machine + refusal rules) — repo module `tools/modeswitch/`, can be written NOW against the state diagram
3. Does CAMP-mode native charging need the car to also see the charge port ECU on its branch? (Yes — charge port lives on Branch A permanently; confirm no open-stack need for it)
4. Selector ergonomics: outside coupler-side panel vs inside galley — decide at SS05 CAD
5. Publish: state diagram + firmware + bench transcript as the flagship's first standalone open-source release (predates the trailer itself)
6. Octovalve positioning without VCFRONT: can the supervisor command the stepper directly, or does the CAMP→DRIVE sequence park the valve before car-brain shutdown? Bench-characterize both paths
7. Coolant loop plumbing across modes: confirm the drive-position valve state serves pack+DU series flow with cabin loop isolated (SS07 Lane-2 diagram update)

---
*v0.1, 2026-07-24. Design-complete pending bench characterization; every claim about BMS/car behavior is superseded by the first bench session. The mux hardware is trivial on purpose — trust the sequence, not the silicon.*
