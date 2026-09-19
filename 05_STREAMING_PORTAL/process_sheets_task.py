import sys
import os
import requests
import csv
import io
import json
import time
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def fetch_sheet(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    reader = list(csv.reader(io.StringIO(resp.text)))
    if not reader:
        return [], []
    header = [c.strip() for c in reader[0][:5]]
    rows = []
    for r in reader[1:]:
        if r and any(r[:2]):
            # Pad to 5 columns: STREAM NAME, URL, CATEGORY, ICON, STATUS
            padded = [r[i].strip() if i < len(r) else "" for i in range(5)]
            rows.append(padded)
    return header, rows

def check_stream_url(url, timeout=8):
    if not url or not url.startswith("http"):
        return False, "Invalid URL"
    
    # Try HEAD request first, if not allowed or 405, do GET with stream
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            code = resp.getcode()
            content_type = resp.headers.get("Content-Type", "").lower()
            # Read first 1024 bytes
            chunk = resp.read(2048).decode("utf-8", errors="replace")
            if code in [200, 206]:
                # Verify it's an HLS manifest or valid media
                if "#EXTM3U" in chunk or "application/vnd.apple.mpegurl" in content_type or "application/x-mpegurl" in content_type or "video/" in content_type or "audio/" in content_type or len(chunk) > 0:
                    return True, f"HTTP {code} - HLS/Media OK"
                return True, f"HTTP {code} - Stream Reachable"
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as e:
        # Some servers return 403 to python user-agent if tokens or referer needed
        # Check if it's one of the known proxyable or Akamai streams
        return False, f"HTTP Error {e.code}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)[:60]}"

def main():
    print("==================================================")
    print("STEP 1: FETCHING SHEET 1 AND SHEET 2 FROM GOOGLE SHEETS")
    print("==================================================")
    h1, r1 = fetch_sheet("IPTV_Playlist")
    h2, r2 = fetch_sheet("Sheet2")
    print(f"Sheet 1 (IPTV_Playlist): {len(r1)} rows")
    print(f"Sheet 2: {len(r2)} rows")

    # Collect all unique URLs to test
    all_urls = set()
    for r in r1:
        if r[1]: all_urls.add(r[1])
    for r in r2:
        if r[1]: all_urls.add(r[1])

    print(f"\nTotal unique URLs across both sheets to test: {len(all_urls)}")
    print("Testing stream reachability concurrently...")

    url_status = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(check_stream_url, u): u for u in all_urls}
        done = 0
        for future in as_completed(future_to_url):
            u = future_to_url[future]
            try:
                is_live, msg = future.result()
                url_status[u] = (is_live, msg)
            except Exception as e:
                url_status[u] = (False, str(e))
            done += 1
            if done % 25 == 0 or done == len(all_urls):
                print(f"  Tested {done}/{len(all_urls)} streams...")

    # Classify Sheet 1
    print("\n==================================================")
    print("STEP 2: ANALYZING SHEET 1 (IPTV_Playlist)")
    print("==================================================")
    sheet1_live = []
    sheet1_dead = []
    for r in r1:
        u = r[1]
        is_live, msg = url_status.get(u, (False, "Not tested"))
        status_str = "Live" if is_live else "Dead"
        r_updated = [r[0], r[1], r[2], r[3], status_str]
        if is_live:
            sheet1_live.append(r_updated)
        else:
            sheet1_dead.append((r_updated, msg))

    print(f"Sheet 1 Live Streams: {len(sheet1_live)}")
    print(f"Sheet 1 Dead Streams (to be moved to Sheet 2): {len(sheet1_dead)}")
    for r, msg in sheet1_dead:
        print(f"  ❌ Moving to Sheet 2: {r[0]} ({r[1]}) -> {msg}")

    # Process Sheet 2:
    # 1. Start with existing Sheet 2 rows
    # 2. Add moved dead rows from Sheet 1
    # 3. Deduplicate by URL
    # 4. Update STATUS to Live or Dead
    print("\n==================================================")
    print("STEP 3: PROCESSING SHEET 2 (DEDUPLICATE & UPDATE STATUS)")
    print("==================================================")
    
    # Track unique URLs in Sheet 2
    sheet2_unique_rows = []
    seen_urls_sheet2 = set()

    # First add rows from Sheet 2
    for r in r2:
        u = r[1].strip()
        if not u:
            continue
        if u in seen_urls_sheet2:
            continue
        seen_urls_sheet2.add(u)
        is_live, msg = url_status.get(u, (False, "Not tested"))
        status_str = "Live" if is_live else "Dead"
        # Preserve or standardize Category & Icon
        cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
        icon = r[3].strip() if len(r) > 3 and r[3].strip() else "📺"
        sheet2_unique_rows.append([r[0].strip(), u, cat, icon, status_str])

    # Now add the dead rows moved from Sheet 1 if not already present
    moved_count = 0
    for r_dead, msg in sheet1_dead:
        u = r_dead[1].strip()
        if u not in seen_urls_sheet2:
            seen_urls_sheet2.add(u)
            sheet2_unique_rows.append([r_dead[0], u, r_dead[2], r_dead[3], "Dead"])
            moved_count += 1
            print(f"  + Added moved dead row to Sheet 2: {r_dead[0]}")
        else:
            # If already present in Sheet 2, make sure its status is Dead
            for row in sheet2_unique_rows:
                if row[1] == u:
                    row[4] = "Dead"
                    break
            print(f"  ~ Dead stream already existed in Sheet 2; marked as Dead: {r_dead[0]}")

    sheet2_live_count = sum(1 for r in sheet2_unique_rows if r[4] == "Live")
    sheet2_dead_count = sum(1 for r in sheet2_unique_rows if r[4] == "Dead")

    print(f"\nSheet 2 After Deduplication + Moving Dead Streams:")
    print(f"  Total Unique Rows in Sheet 2: {len(sheet2_unique_rows)} (Original had {len(r2)})")
    print(f"  Duplicates Removed from Sheet 2: {len(r2) - (len(sheet2_unique_rows) - moved_count)}")
    print(f"  Sheet 2 Live: {sheet2_live_count}")
    print(f"  Sheet 2 Dead: {sheet2_dead_count}")

    # Save local CSV and JSON reports
    os.makedirs("05_STREAMING_PORTAL", exist_ok=True)
    
    # Save clean Sheet 1 (Live only)
    with open("05_STREAMING_PORTAL/Sheet1_Clean_Live_Only.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"])
        writer.writerows(sheet1_live)
    print(f"\nSaved 05_STREAMING_PORTAL/Sheet1_Clean_Live_Only.csv ({len(sheet1_live)} rows)")

    # Save clean Sheet 2 (Deduplicated + Updated Status + Moved Dead Rows)
    with open("05_STREAMING_PORTAL/Sheet2_Deduplicated_Updated.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"])
        writer.writerows(sheet2_unique_rows)
    print(f"Saved 05_STREAMING_PORTAL/Sheet2_Deduplicated_Updated.csv ({len(sheet2_unique_rows)} rows)")

    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sheet1_before": len(r1),
        "sheet1_after_live_only": len(sheet1_live),
        "sheet1_dead_moved": len(sheet1_dead),
        "sheet1_dead_details": [{"name": r[0], "url": r[1], "reason": msg} for r, msg in sheet1_dead],
        "sheet2_before": len(r2),
        "sheet2_after_dedup": len(sheet2_unique_rows),
        "sheet2_live": sheet2_live_count,
        "sheet2_dead": sheet2_dead_count
    }

    with open("05_STREAMING_PORTAL/sync_operation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print("Saved 05_STREAMING_PORTAL/sync_operation_summary.json")

if __name__ == "__main__":
    main()
