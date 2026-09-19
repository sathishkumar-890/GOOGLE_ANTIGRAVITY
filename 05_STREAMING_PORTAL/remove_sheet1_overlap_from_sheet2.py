import requests
import csv
import io
import json
import sys
from urllib.parse import urlparse

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

def norm_url(u):
    p = urlparse(u.strip().rstrip("/"))
    return (p.netloc.lower() + p.path).rstrip("/")

def fetch_sheet(name):
    url = f"https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet={name}"
    r = requests.get(url)
    reader = list(csv.reader(io.StringIO(r.text)))
    header = reader[0][:5]
    rows = [r[:5] for r in reader[1:] if r and any(r[:2])]
    return header, rows

def main():
    print("==================================================")
    print("STEP 1: FETCHING CURRENT SHEET 1 AND SHEET 2")
    print("==================================================")
    h1, s1 = fetch_sheet("IPTV_Playlist")
    h2, s2 = fetch_sheet("Sheet2")
    print(f"Sheet 1 (IPTV_Playlist): {len(s1)} rows")
    print(f"Sheet 2 (Sheet2): {len(s2)} rows")

    # Set of Sheet 1 URLs (normalized for robust comparison)
    s1_urls = set(norm_url(r[1]) for r in s1 if len(r) > 1 and r[1].strip())
    
    print("\n==================================================")
    print("STEP 2: IDENTIFYING OVERLAPPING ROWS TO REMOVE")
    print("==================================================")
    overlapping_rows = []
    filtered_s2 = []

    for r in s2:
        u = norm_url(r[1]) if len(r) > 1 and r[1].strip() else ""
        if u in s1_urls:
            overlapping_rows.append(r)
        else:
            filtered_s2.append(r)

    print(f"Overlapping rows in Sheet 2 found in Sheet 1: {len(overlapping_rows)}")
    print(f"Sheet 2 rows remaining (non-overlapping): {len(filtered_s2)}")

    live_count = sum(1 for r in filtered_s2 if r[4].strip().lower() == "live")
    dead_count = sum(1 for r in filtered_s2 if r[4].strip().lower() == "dead")
    print(f"  - Live in Sheet 2: {live_count}")
    print(f"  - Dead in Sheet 2: {dead_count}")

    # Prepare rows for sync
    headers = ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"]
    sheet2_payload_rows = [headers] + filtered_s2

    # Save to CSV for backup & verification
    out_csv = "05_STREAMING_PORTAL/Sheet2_Non_Overlapping.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sheet2_payload_rows)
    print(f"\nSaved clean non-overlapping dataset to: {out_csv}")

    print("\n==================================================")
    print("STEP 3: SYNCING FILTERED SHEET 2 TO GOOGLE SHEETS")
    print("==================================================")
    payload = {
        "action": "sync_all",
        "sheetName": "Sheet2",
        "rows": sheet2_payload_rows
    }
    
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=90)
    print(f"Webhook Status Code: {resp.status_code}")
    print(f"Webhook Response: {resp.text}")

    if resp.status_code == 200:
        print("\nSUCCESS: Sheet 2 updated directly in Google Sheets!")

if __name__ == "__main__":
    main()
