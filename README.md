# Slipstream

> Intended home: `github.com/divergent-futures/hw-slipstream`

An open-source, aerodynamic, all-electric camping trailer family — designed to be towed behind an EV without destroying its range. Sister project to the [House BUS](https://github.com/divergent-futures/divergent-house-bus): the bus is the dwelling, Slipstream is the weekend base camp.

*A weekend base camp that pulls 75% of its own weight in aerodynamics and the rest in elegance.*

## The idea

One platform, many builds — configured, not customized. The invariant core (~80% of parts) is shared across every trailer: aluminum frame with frame-integrated battery and tanks, 48V Victron electrical spine, NEMA 14-50 universal power interface, composite foam-core shell, sealed aero belly pan, torsion suspension. The fork tree (~20%) is what you choose.

The tier ladder is **build complexity, not range**:

| Tier | ~Price | What it is |
|---|---|---|
| Foamie | $3–12K | Beginner A-frame/foam build, weekend tools |
| Weekend | $30–40K | The reference: 12' pop-up, summer, 12 kWh, sleeps 2 |
| Explorer | $50–60K | 3-season, heat pump, bigger systems |
| Base Camp | $70–90K | 4-season, interior wet stall, expedition tanks |
| Overland | $80–100K | Off-road package + drive assist |
| Range-Neutral | $90–120K | Salvaged Tesla Model 3/Y pack (55–80 kWh) + tongue-force-sensing propulsion — the trailer pushes itself; your car loses ≈0% range. Doubles as a winter home battery (V2H) |

## Repository structure

- `docs/` — design source of truth: the fork-tree handoff (every decision point + rationale), the three-version prototype roadmap (V0.1 bench → V0.5 rolling → V1.0 refined), and vendor sourcing research
- `engineering/` — subsystem design tracks for the V0.1 bench build: battery pack (SS01), electrical core (SS02), pop-up actuation (SS03), composite shell (SS04), frame & chassis (SS05), aero/CFD (SS06) — each traced to its V0.1 gate and the T1–T10 interface map
- `configurator/` — `slipstream.config.json` (the full fork tree in `df-configurator/v1` schema, with compatibility rules and parts/BOM data) and a self-contained HTML configurator — open it in any browser
- `guides/` — follow-along procedural guides for builders; first up: the salvage Tesla donor procurement & teardown guide (safety-gated, sourced against Tesla service manuals + PHMSA guidance)

The configurator data format is shared with the House BUS (see `Configurator_Platform_Spec.md` in that repo); a standalone configurator app consuming both products is planned as its own repository.

## Status

Pre-build, flagship-first: **Build #1 is the Range-Neutral flagship** (salvage CATL LFP pack, ≤3,500 lb loaded behind a Tesla Model Y, 12V house spine off the donor PCS) — see `docs/Flagship_First_Build_Plan_v0_1.md`. The summer reference build remains the configurator default and the future kit. The `guides/` series (donor procurement → pack commissioning → drive-unit bring-up) is the flagship's build path, written for anyone to follow. Numbers in the configurator are researched street prices and first-order estimates; they get replaced by real weights and invoices as the build progresses.

## License

Hybrid open-source: hardware under CERN-OHL-S-2.0, code under MIT, documentation under CC-BY-4.0 — see [LICENSE.md](LICENSE.md).
