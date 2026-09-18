import json
import csv
import sys
from collections import defaultdict

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load Primary
with open("05_STREAMING_PORTAL/primary_sheet_raw.csv", "r", encoding="utf-8") as f:
    primary_channels = [r for r in list(csv.reader(f))[1:] if r and len(r) >= 2 and r[1].strip().startswith("http")]

# Load Sheet2 live results
with open("05_STREAMING_PORTAL/sheet2_live_dead_results.json", "r", encoding="utf-8") as f:
    sheet2_results = json.load(f)

# Load Sheet2 raw
with open("05_STREAMING_PORTAL/sheet2_raw.csv", "r", encoding="utf-8") as f:
    sheet2_raw = [r for r in list(csv.reader(f))[1:] if r and len(r) >= 2 and r[1].strip().startswith("http")]

primary_urls = set(r[1].strip() for r in primary_channels)
live_sheet2_new = [r for r in sheet2_results if r["is_live"] and r["url"] not in primary_urls]

p_names = sorted([r[0].strip() for r in primary_channels])
s_names = [r["name"].strip() for r in live_sheet2_new]

print(f"=== PRIMARY CHANNEL NAMES ({len(p_names)}) ===")
for idx, name in enumerate(p_names, 1):
    print(f" {idx:2d}. {name}")

print(f"\n=== NEW LIVE CHANNELS FROM SHEET2 ({len(s_names)}) ===")
for idx, r in enumerate(live_sheet2_new, 1):
    print(f" {idx:2d}. {r['name']:25s} | {r['url'][:45]}...")

import re
from collections import defaultdict

# Combine primary and new live
all_live = []
for r in primary_channels:
    all_live.append({
        "name": r[0].strip(),
        "url": r[1].strip(),
        "cat": r[2].strip() if len(r) > 2 else "Tamil",
        "icon": r[3].strip() if len(r) > 3 else "📺",
        "source": "primary"
    })

url_to_raw = {}
for r in sheet2_raw:
    u = r[1].strip()
    if u not in url_to_raw:
        url_to_raw[u] = r

for r in live_sheet2_new:
    raw = url_to_raw.get(r["url"], [r["name"], r["url"], "Tamil", "📺"])
    all_live.append({
        "name": raw[0].strip(),
        "url": r["url"],
        "cat": raw[2].strip() if len(raw) > 2 and raw[2].strip() else "Tamil",
        "icon": raw[3].strip() if len(raw) > 3 and raw[3].strip() else "📺",
        "source": "sheet2"
    })

print(f"Total combined live streams: {len(all_live)}")

def get_base_name(name):
    n = name.lower()
    n = re.sub(r"\b(tv|hd|sd|channel|plus)\b", "", n)
    n = re.sub(r"[^a-z0-9]", "", n)
    return n

grouped = defaultdict(list)
for item in all_live:
    b = get_base_name(item["name"])
    grouped[b].append(item)

print("\n--- BASE NAME GROUPS WITH MULTIPLE LIVE STREAMS ---")
for b, items in grouped.items():
    if len(items) > 1:
        print(f"Group [{b}]: {len(items)} streams")
        for it in items:
            print(f"   - {it['name']} ({it['source']}) -> {it['url'][:55]}...")



