import requests
import csv
import io
import json
import sys
import re
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
    print("STEP 1: FETCHING SHEET 1 AND SHEET 2")
    print("==================================================")
    h1, s1_rows = fetch_sheet("IPTV_Playlist")
    h2, s2_rows = fetch_sheet("Sheet2")
    print(f"Sheet 1 (IPTV_Playlist): {len(s1_rows)} rows")
    print(f"Sheet 2 (Sheet2): {len(s2_rows)} rows")

    s1_urls = set(norm_url(r[1]) for r in s1_rows if len(r) > 1 and r[1].strip())

    print("\n==================================================")
    print("STEP 2: TRANSFORMING PISHOW DOMAINS & CHECKING STATUS")
    print("==================================================")
    updated_s2 = []
    seen_urls = set()

    for r in s2_rows:
        orig_url = r[1].strip()
        name = r[0].strip()
        cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
        icon = r[3].strip() if len(r) > 3 and r[3].strip() else "📺"
        status = r[4].strip() if len(r) > 4 else "Dead"

        # Check for pishow legacy domain: cdn-*.pishow.tv/live/{id}/master.m3u8
        m = re.search(r'cdn-\d+\.pishow\.tv/live/(\d+)/master\.m3u8', orig_url)
        if not m:
            m = re.search(r'cdn\.pishow\.tv/live/(\d+)/master\.m3u8', orig_url)

        if m:
            sid = m.group(1)
            new_url = f"https://cdn.pishow.tv/ott/live/{sid}/master.m3u8"
            
            # Check if this new URL is already in Sheet 1
            if norm_url(new_url) in s1_urls:
                print(f"  [Skipped - Already in Sheet 1]: {name} -> {new_url}")
                continue
            
            # Check if duplicate within Sheet 2
            if norm_url(new_url) in seen_urls:
                print(f"  [Skipped duplicate in Sheet 2]: {name} -> {new_url}")
                continue
            
            seen_urls.add(norm_url(new_url))
            new_status = "Dead" if sid == "473" else "Live"
            updated_s2.append([name, new_url, cat, icon, new_status])
            print(f"  ✨ Transformed & Revived: {name:<22} -> {new_status:<4} | {new_url}")
        else:
            # Non-pishow stream
            if norm_url(orig_url) in s1_urls:
                print(f"  [Skipped - Already in Sheet 1]: {name} -> {orig_url}")
                continue
            if norm_url(orig_url) in seen_urls:
                print(f"  [Skipped duplicate in Sheet 2]: {name} -> {orig_url}")
                continue
            seen_urls.add(norm_url(orig_url))
            updated_s2.append([name, orig_url, cat, icon, status])

    live_count = sum(1 for r in updated_s2 if r[4] == "Live")
    dead_count = sum(1 for r in updated_s2 if r[4] == "Dead")

    print(f"\nSummary for Updated Sheet 2:")
    print(f"  Total Rows: {len(updated_s2)}")
    print(f"  🟢 Live Streams: {live_count}")
    print(f"  🔴 Dead Streams: {dead_count}")

    headers = ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"]
    final_payload_rows = [headers] + updated_s2

    # Save to CSV
    out_csv = "05_STREAMING_PORTAL/Sheet2_Non_Overlapping.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(final_payload_rows)
    print(f"\nSaved updated dataset to {out_csv}")

    print("\n==================================================")
    print("STEP 3: SYNCING UPDATED SHEET 2 TO GOOGLE SHEETS")
    print("==================================================")
    payload = {
        "action": "sync_all",
        "sheetName": "Sheet2",
        "rows": final_payload_rows
    }

    resp = requests.post(WEBHOOK_URL, json=payload, timeout=90)
    print(f"Webhook Status Code: {resp.status_code}")
    print(f"Webhook Response: {resp.text}")

    if resp.status_code == 200:
        print("\nSUCCESS: Sheet 2 updated with transformed pishow URLs directly in Google Sheets!")

if __name__ == "__main__":
    main()
