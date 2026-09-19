import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

data = json.load(open("05_STREAMING_PORTAL/auditor_engine_results.json", encoding="utf-8"))

section = sys.argv[1] if len(sys.argv) > 1 else "s1_p1"

if section == "s1_p1":
    print("==========================================================================================")
    print("SHEET 1 - PART 1 (Rows 1 to 40)")
    print("==========================================================================================")
    s1 = [r for r in data if r["sheet"] == "Sheet1"]
    for r in s1[:40]:
        stat = r["new_status"]
        cat = r["detected_category"]
        old = r["old_cat"]
        txt = r["transcript"]
        nm = r["name"]
        snip = f" | Spoken: '{txt[:30]}...'" if txt else f" ({r['notes'][:40]})"
        change = f" [CHANGED: {old} -> {cat}]" if cat != old and stat == "Live" else ""
        print(f"#{r['index']:02d} [{stat:<4}] [{cat:<10}] {nm:<22} (Old: {old:<8}){snip}{change}")

elif section == "s1_p2":
    print("==========================================================================================")
    print("SHEET 1 - PART 2 (Rows 41 to 78)")
    print("==========================================================================================")
    s1 = [r for r in data if r["sheet"] == "Sheet1"]
    for r in s1[40:]:
        stat = r["new_status"]
        cat = r["detected_category"]
        old = r["old_cat"]
        txt = r["transcript"]
        nm = r["name"]
        snip = f" | Spoken: '{txt[:30]}...'" if txt else f" ({r['notes'][:40]})"
        change = f" [CHANGED: {old} -> {cat}]" if cat != old and stat == "Live" else ""
        print(f"#{r['index']:02d} [{stat:<4}] [{cat:<10}] {nm:<22} (Old: {old:<8}){snip}{change}")

elif section == "s2":
    print("==========================================================================================")
    print("SHEET 2 (Rows 1 to 48)")
    print("==========================================================================================")
    s2 = [r for r in data if r["sheet"] == "Sheet2"]
    for r in s2:
        stat = r["new_status"]
        cat = r["detected_category"]
        old = r["old_cat"]
        txt = r["transcript"]
        nm = r["name"]
        snip = f" | Spoken: '{txt[:30]}...'" if txt else f" ({r['notes'][:40]})"
        change = f" [CHANGED: {old} -> {cat}]" if cat != old and stat == "Live" else ""
        print(f"#{r['index']:02d} [{stat:<4}] [{cat:<10}] {nm:<22} (Old: {old:<8}){snip}{change}")
