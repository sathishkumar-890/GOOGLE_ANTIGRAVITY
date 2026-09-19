import requests
import csv
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

r1 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist")
s1 = list(csv.reader(io.StringIO(r1.text)))[1:]

r2 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2")
s2 = list(csv.reader(io.StringIO(r2.text)))[1:]

def clean(n):
    # Remove 'tv', 'hd', numbers, spaces, punctuation
    c = re.sub(r'\b(tv|hd)\b', '', n, flags=re.IGNORECASE)
    return re.sub(r'[^a-zA-Z0-9]+', '', c.lower())

s1_names = {r[0].strip().lower(): r[0].strip() for r in s1}
s1_clean = {}
for r in s1:
    k = clean(r[0])
    if k not in s1_clean:
        s1_clean[k] = []
    s1_clean[k].append(r[0].strip())

print(f"Sheet 1 streams count: {len(s1)}")
print(f"Sheet 2 streams count: {len(s2)}")
print("\n--- Name Comparison ---")
for r in s2:
    nm = r[0].strip()
    nm_lower = nm.lower()
    c = clean(nm)
    
    if nm_lower in s1_names:
        print(f"  [EXACT MATCH]: Sheet 2 '{nm}' == Sheet 1 '{s1_names[nm_lower]}'")
    elif c in s1_clean:
        print(f"  [BASE MATCH]:  Sheet 2 '{nm}' matches Sheet 1 {s1_clean[c]}")
    else:
        print(f"  [UNIQUE]:      Sheet 2 '{nm}'")
