import requests
import csv
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

r1 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist")
s1 = list(csv.reader(io.StringIO(r1.text)))
s1_rows = [r for r in s1[1:] if r and any(r[:2])]

r2 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2")
s2 = list(csv.reader(io.StringIO(r2.text)))
s2_rows = [r for r in s2[1:] if r and any(r[:2])]

s2_live = [r for r in s2_rows if len(r)>4 and r[4].strip() == "Live"]
s2_dead = [r for r in s2_rows if len(r)>4 and r[4].strip() == "Dead"]

print(f"Current Sheet 1 rows: {len(s1_rows)}")
print(f"Current Sheet 2 Live rows: {len(s2_live)}")
print(f"Current Sheet 2 Dead rows: {len(s2_dead)}")

# Check name matches
def normalize_name(n):
    # Remove 'tv', 'hd', punctuation, and whitespace
    clean = re.sub(r'\b(tv|hd)\b', '', n, flags=re.IGNORECASE)
    clean = re.sub(r'[^a-zA-Z0-9]+', '', clean.lower())
    return clean

s1_names_norm = {}
for idx, r in enumerate(s1_rows):
    norm = normalize_name(r[0])
    s1_names_norm[norm] = (idx, r[0].strip())

print("\n--- Matching Check ---")
for r in s2_live:
    name = r[0].strip()
    norm = normalize_name(name)
    if norm in s1_names_norm:
        orig_idx, orig_name = s1_names_norm[norm]
        print(f"MATCH FOUND: Sheet 1 '{orig_name}' (row {orig_idx+1}) <==> Sheet 2 '{name}'")
    else:
        print(f"Unique: '{name}'")
