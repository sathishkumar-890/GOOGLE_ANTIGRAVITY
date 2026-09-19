import sys
import requests
import csv
import io
import json

sys.stdout.reconfigure(encoding="utf-8")

def get_sheet_data(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    r = requests.get(url)
    reader = list(csv.reader(io.StringIO(r.text)))
    header = reader[0][:5]
    rows = []
    for row in reader[1:]:
        if row and any(row[:2]):
            rows.append(row[:5])
    return header, rows

h1, r1 = get_sheet_data('IPTV_Playlist')
print(f"=== SHEET 1: IPTV_Playlist === (Total: {len(r1)})")
print("Header:", h1)
for i in range(min(5, len(r1))):
    print(r1[i])

h2, r2 = get_sheet_data('Sheet2')
print(f"\n=== SHEET 2: Sheet2 === (Total: {len(r2)})")
print("Header:", h2)
for i in range(min(5, len(r2))):
    print(r2[i])

# Analyze duplicates in Sheet2
urls_sheet2 = [r[1].strip() for r in r2 if len(r) > 1 and r[1].strip()]
unique_urls_sheet2 = set()
duplicate_urls_sheet2 = set()
for u in urls_sheet2:
    if u in unique_urls_sheet2:
        duplicate_urls_sheet2.add(u)
    else:
        unique_urls_sheet2.add(u)

print(f"\nSheet 2 total URLs: {len(urls_sheet2)}")
print(f"Sheet 2 unique URLs: {len(unique_urls_sheet2)}")
print(f"Sheet 2 duplicate URLs count: {len(duplicate_urls_sheet2)}")

# Check overlap between Sheet 1 and Sheet 2
urls_sheet1 = set(r[1].strip() for r in r1 if len(r) > 1 and r[1].strip())
overlap = urls_sheet1.intersection(unique_urls_sheet2)
print(f"\nOverlap URLs between Sheet 1 and Sheet 2: {len(overlap)}")
