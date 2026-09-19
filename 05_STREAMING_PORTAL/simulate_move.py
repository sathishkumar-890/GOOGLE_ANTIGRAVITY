import requests
import csv
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

r1 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist")
s1_raw = list(csv.reader(io.StringIO(r1.text)))
s1_header = s1_raw[0][:5]
s1_rows = [r[:5] for r in s1_raw[1:] if r and any(r[:2])]

r2 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2")
s2_raw = list(csv.reader(io.StringIO(r2.text)))
s2_header = s2_raw[0][:5]
s2_rows = [r[:5] for r in s2_raw[1:] if r and any(r[:2])]

s2_live = [r for r in s2_rows if len(r)>4 and r[4].strip() == "Live"]
s2_dead = [r for r in s2_rows if len(r)>4 and r[4].strip() == "Dead"]

print(f"Sheet 1 current: {len(s1_rows)} streams")
print(f"Sheet 2 current: {len(s2_rows)} streams ({len(s2_live)} Live, {len(s2_dead)} Dead)")

# Detect collisions
def norm_key(name):
    c = re.sub(r'\b(tv|hd)\b', '', name, flags=re.IGNORECASE)
    return re.sub(r'[^a-zA-Z0-9]+', '', c.lower())

# Build mapping of norm_key to s1 rows
s1_dict = {}
for idx, r in enumerate(s1_rows):
    k = norm_key(r[0])
    s1_dict[k] = idx

# Prepare updated Sheet 1 rows
new_s1_rows = [list(r) for r in s1_rows]

moved_to_s1 = []
for r in s2_live:
    new_r = list(r)
    k = norm_key(new_r[0])
    if k in s1_dict:
        s1_idx = s1_dict[k]
        orig_s1_name = new_s1_rows[s1_idx][0]
        # Rename both with TV1 and TV2
        base_name = re.sub(r'\s*\b(tv\d*|hd)\b\s*', ' ', orig_s1_name, flags=re.IGNORECASE).strip()
        if not base_name:
            base_name = orig_s1_name
        
        # Update existing Sheet 1 row
        new_s1_rows[s1_idx][0] = f"{base_name} TV1"
        # Name the moved row
        new_r[0] = f"{base_name} TV2"
        print(f"Collision resolved: '{orig_s1_name}' -> '{new_s1_rows[s1_idx][0]}' AND '{r[0]}' -> '{new_r[0]}'")
    moved_to_s1.append(new_r)

# Combine
final_sheet1 = [s1_header] + new_s1_rows + moved_to_s1

# Final Sheet 2 has only the dead channels (live moved out)
final_sheet2 = [s2_header] + s2_dead

print(f"\nFinal Sheet 1 streams: {len(final_sheet1)-1} (all Live)")
print(f"Final Sheet 2 streams: {len(final_sheet2)-1} (all Dead)")

print("\n--- Final Sheet 1 Sample Preview (last 10) ---")
for i, r in enumerate(final_sheet1[-10:], len(final_sheet1)-10):
    print(f"{i:2d}. {r[0]:<25} | {r[2]:<10} | {r[4]:<5} | {r[1][:40]}")
