#!/usr/bin/env node
// df-configurator/v1 stress-test suite — run: node tools/config-test/test.mjs
// Validates structure, sweeps every option, fuzzes N random configs, checks
// rule reachability + option viability, reports per-tier BOM coverage, and
// verifies the generated HTML embeds the exact config JSON.
import { readFileSync, existsSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = join(HERE, "..", "..");
const FUZZ_N = parseInt(process.env.FUZZ_N || "50000", 10);
let failures = 0;
const fail = (msg) => { failures++; console.log("  ❌ " + msg); };
const ok = (msg) => console.log("  ✓ " + msg);

// ---- engine-equivalent core (keep in sync with Configurator_Engine.template.html) ----
function matches(cond, state) {
  return Object.entries(cond).every(([k, v]) => Array.isArray(v) ? v.includes(state[k]) : state[k] === v);
}
function computeState(C, state) {
  const sums = {}, mults = {}, sets = {};
  for (const f of C.forks) {
    const o = f.options.find(o => o.id === state[f.key]);
    for (const [k, v] of Object.entries(o.effects || {})) {
      if (k.endsWith("Mult")) mults[k] = (mults[k] ?? 1) * v; else sums[k] = (sums[k] || 0) + v;
    }
    Object.assign(sets, o.sets || {});
  }
  const metrics = {};
  for (const m of (C.ui?.metrics || [])) {
    let v = (m.base || 0) + (m.addKey ? (sums[m.addKey] || 0) : 0);
    if (m.multKey && mults[m.multKey]) v *= mults[m.multKey];
    metrics[m.id] = Math.round(v);
  }
  const forbid = [], warn = [];
  for (const r of (C.rules || [])) (matches(r.when, state) ? (r.type === "forbid" ? forbid : warn) : []).push(r.id);
  return { sums, mults, sets, metrics, forbid, warn };
}
function bomFor(C, state) {
  const drop = new Set(), skip = new Set();
  (C.ui?.suppressBasePartIds || []).forEach(r => { if (matches(r.when, state)) r.ids.forEach(i => drop.add(i)); });
  (C.ui?.suppressForkParts || []).forEach(r => { if (matches(r.when, state)) r.forks.forEach(k => skip.add(k)); });
  const supAll = C.ui?.suppressBaseParts && matches(C.ui.suppressBaseParts, state);
  const bom = supAll ? [] : (C.product.baseParts || []).filter(p => !drop.has(p.id));
  for (const f of C.forks) {
    if (skip.has(f.key)) continue;
    const o = f.options.find(o => o.id === state[f.key]);
    (o.parts || []).forEach(p => bom.push(p));
  }
  return bom;
}
const defaults = (C) => Object.fromEntries(C.forks.map(f => [f.key, (f.options.find(o => o.default) || f.options[0]).id]));

// ---- per-product test battery ----
function testProduct(name, cfgPath, htmlPath, archetypes) {
  console.log(`\n═══ ${name} ═══`);
  const raw = readFileSync(cfgPath, "utf8");
  const C = JSON.parse(raw);

  // 1. structure
  const forkKeys = new Set();
  for (const f of C.forks) {
    if (forkKeys.has(f.key)) fail(`duplicate fork key ${f.key}`); forkKeys.add(f.key);
    const ids = new Set();
    for (const o of f.options) { if (ids.has(o.id)) fail(`duplicate option ${f.key}:${o.id}`); ids.add(o.id); }
    const defs = f.options.filter(o => o.default);
    if (defs.length !== 1) fail(`fork ${f.key}: ${defs.length} defaults`);
    else if (Object.keys(defs[0].effects || {}).length) fail(`fork ${f.key}: default has nonzero effects`);
    if (!(C.categories || []).some(c => c.id === f.category)) fail(`fork ${f.key}: unknown category ${f.category}`);
  }
  const refCheck = (id, when) => Object.entries(when).forEach(([k, v]) => {
    const f = C.forks.find(f => f.key === k);
    if (!f) return fail(`${id}: unknown fork ${k}`);
    (Array.isArray(v) ? v : [v]).forEach(o => { if (!f.options.some(x => x.id === o)) fail(`${id}: unknown option ${k}:${o}`); });
  });
  (C.rules || []).forEach(r => refCheck("rule " + r.id, r.when));
  (C.profiles || []).filter(p => p.match).forEach(p => refCheck("profile " + p.id, p.match));
  (C.tiers || []).forEach(t => refCheck("tier " + t.id, t.match));
  (C.ui?.suppressForkParts || []).forEach((r, i) => { refCheck("suppressForkParts#" + i, r.when); r.forks.forEach(k => { if (!forkKeys.has(k)) fail(`suppressForkParts#${i}: unknown fork ${k}`); }); });
  (C.ui?.suppressBasePartIds || []).forEach((r, i) => { refCheck("suppressBasePartIds#" + i, r.when); r.ids.forEach(id => { if (!(C.product.baseParts || []).some(p => p.id === id)) fail(`suppressBasePartIds#${i}: unknown basePart ${id}`); }); });
  if (raw.includes("</")) fail("config contains '</' sequence (breaks inline <script> embedding)");
  ok(`structure: ${C.forks.length} forks, ${(C.rules || []).length} rules, ${(C.profiles || []).length} profiles, ${(C.tiers || []).length} tiers`);

  // 2. defaults sanity + single-option sweep
  const d = defaults(C);
  const dRes = computeState(C, d);
  if (dRes.forbid.length) fail(`DEFAULTS trigger forbids: ${dRes.forbid}`);
  for (const [k, v] of Object.entries(dRes.metrics)) if (!Number.isFinite(v)) fail(`default metric ${k} not finite`);
  ok(`defaults legal; metrics ${JSON.stringify(dRes.metrics)}`);
  let sweepCount = 0, sweepForbids = 0;
  for (const f of C.forks) for (const o of f.options) {
    const s = { ...d, [f.key]: o.id };
    const r = computeState(C, s); sweepCount++;
    if (r.forbid.length) sweepForbids++;
    for (const [k, v] of Object.entries(r.metrics)) if (!Number.isFinite(v)) fail(`sweep ${f.key}:${o.id} metric ${k} not finite`);
    bomFor(C, s).forEach(p => { if (p.estUsd !== undefined && (!Number.isFinite(p.estUsd) || p.estUsd < 0)) fail(`bad estUsd on ${p.id}`); });
  }
  ok(`single-option sweep: ${sweepCount} configs, ${sweepForbids} legitimately forbidden vs defaults`);

  // 3. fuzz: no crashes, finite metrics, rule reachability, option viability
  let rnd = 12345; const rand = () => (rnd = (rnd * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  const ruleHits = Object.fromEntries((C.rules || []).map(r => [r.id, 0]));
  const optLegal = {}; C.forks.forEach(f => f.options.forEach(o => optLegal[f.key + ":" + o.id] = 0));
  let legal = 0, minDry = Infinity, maxDry = -Infinity;
  const dryId = C.ui?.metrics?.find(m => m.id === "dry" || m.id === "curb")?.id;
  for (let i = 0; i < FUZZ_N; i++) {
    const s = {}; C.forks.forEach(f => s[f.key] = f.options[Math.floor(rand() * f.options.length)].id);
    let r;
    try { r = computeState(C, s); bomFor(C, s); } catch (e) { fail(`fuzz crash on ${JSON.stringify(s)}: ${e.message}`); break; }
    r.forbid.forEach(id => ruleHits[id] !== undefined && ruleHits[id]++);
    r.warn.forEach(id => ruleHits[id] !== undefined && ruleHits[id]++);
    for (const v of Object.values(r.metrics)) if (!Number.isFinite(v)) { fail(`fuzz non-finite metric in ${JSON.stringify(s)}`); break; }
    if (dryId) { minDry = Math.min(minDry, r.metrics[dryId]); maxDry = Math.max(maxDry, r.metrics[dryId]); }
    if (!r.forbid.length) { legal++; C.forks.forEach(f => optLegal[f.key + ":" + s[f.key]]++); }
  }
  ok(`fuzz ${FUZZ_N}: ${legal} legal (${(100 * legal / FUZZ_N).toFixed(1)}%), ${dryId || "wt"} range ${minDry}–${maxDry} lb`);
  if (dryId && minDry <= 0) fail(`weight metric can go non-positive (${minDry})`);
  const dead = Object.entries(ruleHits).filter(([, n]) => n === 0).map(([id]) => id);
  if (dead.length) fail(`unreachable rules (never fired in fuzz): ${dead.join(", ")}`); else if ((C.rules || []).length) ok("every rule fired at least once (reachable)");
  const unviable = Object.entries(optLegal).filter(([, n]) => n === 0).map(([k]) => k);
  if (unviable.length) fail(`options never legal in any fuzzed config: ${unviable.join(", ")}`); else ok("every option appears in ≥1 legal config (viable)");

  // 4. archetype BOM coverage (the early/late check)
  if (archetypes) {
    console.log("  — tier archetype coverage —");
    for (const [label, over] of Object.entries(archetypes)) {
      const s = { ...d, ...over };
      const r = computeState(C, s);
      const bom = bomFor(C, s);
      const known = bom.filter(p => p.estUsd), tbd = bom.length - known.length;
      const usd = known.reduce((a, p) => a + p.estUsd * p.qty, 0);
      const flag = r.forbid.length ? ` ❌ FORBIDS: ${r.forbid}` : "";
      console.log(`    ${label.padEnd(22)} ${String(bom.length).padStart(2)} parts, $${usd.toLocaleString().padStart(7)} researched, ${tbd} TBD${flag}`);
      if (r.forbid.length) failures++;
    }
  }

  // 5. HTML integrity: generated file embeds exactly this config
  if (htmlPath && existsSync(htmlPath)) {
    const html = readFileSync(htmlPath, "utf8");
    if (html.includes("__CONFIG__")) fail("HTML still contains placeholder");
    else if (!html.trimEnd().endsWith("</html>")) fail("HTML FILE TRUNCATED (missing </html>) - regenerate from engine template");
    else if (!/<\/script>/.test(html)) fail("HTML missing closing </script> - truncated mid-script");
    else if (!html.includes(raw.trim())) fail("HTML embedded config != config file (regenerate from engine template)");
    else ok("HTML complete (closing tags present) and embeds the exact current config");
  }
  return C;
}

// ---- run ----
testProduct("SLIPSTREAM", join(REPO, "configurator/slipstream.config.json"),
  join(REPO, "configurator/Slipstream_Configurator.html"), {
  "foamie minimal":   { build_class: "foamie", roof_type: "fixed", battery: "kwh8", cooling: "none", solar: "sol600", media: "none", awning: "none", water_heater: "none", shower: "none", fridge: "none", cabinetry: "minimal", toilet: "dry", sink: "none" },
  "foamie kit":       { build_class: "foamie", roof_type: "fixed", battery: "kwh8", solar: "sol600", fridge: "dualzone", cooling: "none" },
  "weekend reference": {},
  "explorer 3-season": { season: "s3", insulation: "in15", heating: "heatpump", cooling: "none", battery: "kwh16", shower: "outdoor_enc" },
  "base camp 4-season": { season: "s4", insulation: "in2", heating: "heatpump", cooling: "none", box_length: "b15", shower: "wet_stall", gray_water: "g15", water_heater: "tank6", tow_vehicle: "lightning", bed_size: "queen" },
  "overland":          { drivetrain: "awd", offroad: "pkg", use_case: "expedition", tow_vehicle: "r1t", season: "s3", insulation: "in15", heating: "ptc", box_length: "b15" },
  "flagship (TJ)":     { propulsion_pack: "tesla_lfp", drivetrain: "range_neutral", battery: "pcs12v", home_power: "seasonal_dock", hv_charging: "donor_pcs" },
  "flagship max":      { propulsion_pack: "tesla_2170", drivetrain: "range_neutral", battery: "pcs12v", home_power: "seasonal_dock", hv_charging: "elcon", box_length: "b15", tow_vehicle: "lightning", season: "s3", insulation: "in15", heating: "heatpump", cooling: "none" },
});

const busPath = join(REPO, "..", "01_Roadmap_and_Strategy", "house-bus.config.json");
if (existsSync(busPath)) {
  testProduct("HOUSE BUS", busPath, join(REPO, "..", "01_Roadmap_and_Strategy", "House_BUS_Configurator.html"), {
    "stay-local budget": { tier: "entry" },
    "default mid":       {},
    "overlander":        { drive: "awd", solar: "wings", chp: "chp35" },
    "cross-country max": { tier: "high", chem: "lfp", bath: "sig", chp: "chp5", solar: "wings", rear: "toy" },
  });
} else console.log("\n(HOUSE BUS config not found at expected sibling path — skipped; run from full workspace to include it)");

console.log(failures ? `\n════ ${failures} FAILURE(S) ════` : "\n════ ALL PASS ════");
process.exit(failures ? 1 : 0);
