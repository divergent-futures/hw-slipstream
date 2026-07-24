#!/usr/bin/env python3
"""
donor-watch — salvage Tesla donor watchlist for the Slipstream flagship build.

Watches salvage-auction listings for Model 3/Y donors matching the project's
procurement filter (guides/Donor_Procurement_and_Teardown_Guide_v0_1.md),
tracks auction countdowns, and notifies when a match is new or auctions soon.

Design notes (read README.md first):
- Fetchers are pluggable and EVERY fetch failure is non-fatal: auction sites
  rotate bot protection, so a blocked source degrades to a "check manually"
  line in the report instead of crashing the run.
- This tool never bypasses logins or CAPTCHAs. Keep the schedule polite
  (default: every 6 h). You bid with your own account; this only watches.
- State lives in watchlist.json next to this script (committed by the
  GitHub Actions workflow so diffs are visible in repo history).

Usage:  python3 donor_watch.py [--config config.json] [--dry-run]
Deps:   pip install requests
License: MIT (see repo LICENSE.md)
"""

import argparse, json, re, smtplib, sys, time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

HERE = Path(__file__).parent
UA = {"User-Agent": "Mozilla/5.0 (donor-watch; open-source salvage watchlist; low-frequency personal use)"}


# ---------------------------------------------------------------- filter ----

def score_lot(lot, cfg):
    """Apply the Guide #1 donor filter. Returns (verdict, reasons).
    verdict: 'match' | 'reject' | 'review'."""
    reasons = []
    dmg = (lot.get("damage") or "").lower()
    dmg2 = (lot.get("damage_secondary") or "").lower()
    vin = (lot.get("vin") or "").upper()
    title = (lot.get("title_type") or "").lower()

    # hard rejects (flood is non-negotiable; everything else is human-checkable)
    for bad in ("flood", "water", "burn", "fire"):
        if bad in dmg or bad in dmg2:
            return "reject", [f"damage includes '{bad}'"]
    if len(vin) >= 11 and vin[10] == "A":
        return "reject", ["Austin-built (VIN pos 11 = A): 4680 structural pack"]
    for bad in ("undercarriage", "side"):
        if bad in dmg:
            reasons.append(f"inspect-first geometry ({dmg}) - human review, not auto-reject")

    # positives
    if "hail" in dmg or "hail" in dmg2:
        reasons.append("HAIL total - cosmetic write-off, pack/drivetrain/thermal all likely intact (top-tier donor)")
    if "rear" in dmg:
        reasons.append("REAR HIT = IDEAL V1 PACK DONOR (D-F7): pack + car-brain + HVAC/radiator/screen all intact; sacrificed rear subframe/DU comes from the split drive-donor")
    if "front" in dmg:
        reasons.append("FRONT HIT = DU/SUBFRAME DONOR ONLY: car-brain + HVAC + radiator harvest lost - do NOT buy as the pack donor (D-F6 needs an intact front end)")
    yr0 = lot.get("year") or 0
    trim0 = (lot.get("trim") or "").lower()
    is_rwd = any(t in trim0 for t in ("rwd", "standard", "sr"))
    if 2022 <= yr0 <= 2024 and is_rwd and "model 3" in (lot.get("model") or "").lower():
        reasons.append("TRACK-1 FLAGSHIP PACK DONOR: 2022-2024 Model 3 RWD = CATL LFP (Gen2 60 kWh - same pack design still shipping new in 2026; US LFP window closed Oct 2024, so this IS the newest US LFP)")
    elif yr0 >= 2025 or (yr0 >= 2023 and not any(t in trim0 for t in ("rwd",))):
        reasons.append("TRACK-1B NICKEL PACK DONOR (co-primary, first-good-donor-wins): 2023+ LR/Standard 2170 = +15-20 kWh vs LFP, +88-200 lb, needs 60-80% SoC dock discipline; newest cells, best US availability")
    elif 2021 <= yr0 <= 2023:
        reasons.append("2021-2023: proven-DU-path donor (Maguire board demonstrated) - the drive-unit half of the split-donor strategy")
    if lot.get("run_drive"):
        reasons.append("Run and Drive")
    if len(vin) >= 11 and vin[10] == "F":
        reasons.append("Fremont-built")
    yr = lot.get("year") or 0
    model = (lot.get("model") or "").lower()
    if "model 3" in model and yr >= 2021 and any(t in (lot.get("trim") or "").lower() for t in ("standard", "rwd", "sr")):
        reasons.append("likely CATL LFP pack (preferred donor)")
    if "parts only" in title or "non-repairable" in title:
        reasons.append("parts-only title (cheaper; check your state's buyer rules)")

    risky = any(r.startswith("inspect-first") for r in reasons)
    good = any(r.startswith(("REAR", "HAIL", "Run", "Fremont", "likely", "TRACK-1", "2021-2023")) for r in reasons)
    if risky:
        return "review", reasons  # side/undercarriage ALWAYS gets human eyes, however good the rest looks
    return ("match" if good else "review"), reasons


# -------------------------------------------------------------- fetchers ----

def fetch_copart(cfg):
    """Copart public search endpoint. Frequently behind Incapsula — expect
    failures; that's fine. Adjust filters at https://www.copart.com after
    changing this. Returns list of normalized lots."""
    url = "https://www.copart.com/public/lots/search"
    payload = {
        "query": cfg.get("query", "tesla model 3"),
        "filter": {"MISC": [f"#VehicleTypeCode:VEHTYPE_V", f"#LotYearFrom:{cfg.get('year_min', 2018)}"]},
        "searchName": "", "watchListOnly": False, "freeFormSearch": False,
        "page": 0, "size": 50, "start": 0,
    }
    r = requests.post(url, json=payload, headers={**UA, "Content-Type": "application/json"}, timeout=30)
    r.raise_for_status()
    out = []
    for it in r.json().get("data", {}).get("results", {}).get("content", []):
        out.append({
            "source": "copart", "lot_id": str(it.get("lotNumberStr") or it.get("ln")),
            "year": it.get("lcy"), "model": f"{it.get('mkn','')} {it.get('lm','')}".strip(),
            "trim": it.get("series") or "", "vin": it.get("fv") or "",
            "damage": it.get("dd") or "", "damage_secondary": it.get("sdd") or "",
            "run_drive": "run" in (it.get("lcd") or "").lower(),
            "title_type": it.get("td") or "", "yard": it.get("yn") or "",
            "current_bid": it.get("hb"), "auction_utc": it.get("ad"),
            "url": f"https://www.copart.com/lot/{it.get('lotNumberStr') or it.get('ln')}",
        })
    return out


def fetch_iaai(cfg):
    """IAAI public search. Endpoint shape changes; treat as best-effort."""
    url = "https://www.iaai.com/Search"
    r = requests.get(url, params={"Keyword": cfg.get("query", "tesla model 3")}, headers=UA, timeout=30)
    r.raise_for_status()
    # IAAI renders server-side; a robust parser needs maintenance. Extract
    # coarse lot links so at least discovery works when reachable.
    out = []
    for m in re.finditer(r'href="(/VehicleDetail/(\d+)[^"]*)"', r.text):
        out.append({"source": "iaai", "lot_id": m.group(2), "url": "https://www.iaai.com" + m.group(1),
                    "model": cfg.get("query", ""), "damage": "", "needs_manual_review": True})
    return out


FETCHERS = {"copart": fetch_copart, "iaai": fetch_iaai}


# ---------------------------------------------------------------- notify ----

def notify_ntfy(cfg, subject, body):
    topic = cfg.get("ntfy_topic")
    if not topic:
        return
    requests.post(f"https://ntfy.sh/{topic}", data=body.encode(),
                  headers={**UA, "Title": subject, "Tags": "car,battery"}, timeout=15)


def notify_email(cfg, subject, body):
    em = cfg.get("email") or {}
    if not em.get("smtp_host"):
        return
    msg = MIMEText(body)
    msg["Subject"], msg["From"], msg["To"] = subject, em["from"], em["to"]
    with smtplib.SMTP_SSL(em["smtp_host"], em.get("smtp_port", 465)) as s:
        s.login(em["user"], em["password"])
        s.send_message(msg)


# ------------------------------------------------------------------ main ----

def hours_until(auction_utc):
    if not auction_utc:
        return None
    try:
        ts = auction_utc / 1000 if auction_utc > 1e12 else auction_utc
        return (datetime.fromtimestamp(ts, tz=timezone.utc) - datetime.now(timezone.utc)).total_seconds() / 3600
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(HERE / "config.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--approve", action="append", default=[], metavar="SOURCE:LOTID", help="mark a lot human-approved (tracked + urgent reminders)")
    ap.add_argument("--reject", action="append", default=[], metavar="SOURCE:LOTID", help="strike a lot from the list")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    state_path = HERE / "watchlist.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"lots": {}}
    # human verdicts first (these work offline, no fetching)
    for key in args.approve:
        state["lots"].setdefault(key, {})["human"] = "approved"
    for key in args.reject:
        state["lots"].setdefault(key, {})["human"] = "rejected"
    if args.approve or args.reject:
        state_path.write_text(json.dumps(state, indent=2))
        print("verdicts recorded:", ", ".join(args.approve + ["-" + r for r in args.reject]))
        if not (len(sys.argv) > 1 and "--dry-run" in sys.argv):
            return

    lots, failures = [], []
    for name in cfg.get("sources", ["copart", "iaai"]):
        try:
            found = FETCHERS[name](cfg)
            lots.extend(found)
            time.sleep(3)  # politeness
        except Exception as e:
            failures.append(f"{name}: {type(e).__name__} — check manually at the site")

    new_matches, urgent, lines = [], [], []
    for lot in lots:
        verdict, reasons = score_lot(lot, cfg)
        key = f"{lot['source']}:{lot['lot_id']}"
        prev = state["lots"].get(key, {})
        known = bool(prev)
        human = prev.get("human", "pending")
        state["lots"][key] = {"seen": datetime.now(timezone.utc).isoformat(), "verdict": verdict, "human": human, **lot}
        if verdict == "reject" or human == "rejected":
            continue
        h = hours_until(lot.get("auction_utc"))
        desc = (f"{lot.get('year','?')} {lot.get('model','?')} | {lot.get('damage','?')}"
                f" | {lot.get('yard','?')} | bid ${lot.get('current_bid','?')}"
                f" | {'auctions in %.0f h' % h if h and h > 0 else 'auction time unknown'}"
                f" | {', '.join(reasons)} | {lot['url']}")
        tag = {"approved": "[APPROVED] ", "pending": "[NEEDS REVIEW] "}.get(human, "")
        if not known:
            new_matches.append(tag + desc)
        # urgent countdown reminders: approved always; pending flagged so the human decides in time
        if h is not None and 0 < h <= cfg.get("urgent_hours", 48):
            urgent.append(tag + desc)

    if urgent:
        lines.append("🚨 AUCTIONS WITHIN %d H:\n" % cfg.get("urgent_hours", 48) + "\n".join(urgent))
    if new_matches:
        lines.append("🆕 NEW MATCHES:\n" + "\n".join(new_matches))
    if failures:
        lines.append("⚠️ SOURCES UNREACHABLE (bot protection is normal — check manually):\n" + "\n".join(failures))
    report = "\n\n".join(lines) or "No new matching donors; no urgent auctions."
    print(report)

    if not args.dry_run:
        state_path.write_text(json.dumps(state, indent=2))
        if urgent or new_matches:
            subject = f"donor-watch: {len(urgent)} urgent / {len(new_matches)} new"
            notify_ntfy(cfg, subject, report)
            notify_email(cfg, subject, report)


if __name__ == "__main__":
    main()
