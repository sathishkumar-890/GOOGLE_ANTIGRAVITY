import json
import csv

with open("05_STREAMING_PORTAL/verification_results_full.json", "r", encoding="utf-8") as f:
    results = json.load(f)

playing = [r for r in results if r["playing"]]
offline = [r for r in results if not r["playing"]]

print(f"Total streams verified: {len(results)}")
print(f"Actively playing: {len(playing)}")
print(f"Offline / not playing: {len(offline)}\n")

print("=== 61 VERIFIED ACTIVELY PLAYING CHANNELS ===")
for idx, p in enumerate(playing, 1):
    res = p.get("resolution", "")
    cur_t = p.get("currentTime", "")
    print(f"{idx:2d}. Row {p['row']:3d} | [{res:9s} | {cur_t}s] | {p['name']:25s} | {p['url'][:55]}...")

print("\n=== TOP OFFLINE REASONS ===")
from collections import Counter
reasons = Counter([o["reason"] for o in offline])
for r, count in reasons.most_common():
    print(f" - {count:3d} streams: {r}")
