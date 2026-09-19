import sys
import re
import urllib.request
import ssl
import csv
import io
import requests

sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def test_url(url, timeout=7):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            code = resp.getcode()
            content_type = resp.headers.get("Content-Type", "").lower()
            chunk = resp.read(2048).decode("utf-8", errors="replace")
            if code in [200, 206] and ("#EXTM3U" in chunk or "mpegurl" in content_type or len(chunk) > 20):
                return True, code, "Live HLS"
            return False, code, "Empty or unexpected content"
    except urllib.error.HTTPError as e:
        return False, e.code, f"HTTP Error {e.code}"
    except Exception as e:
        return False, 0, str(e)[:50]

def main():
    # Fetch Sheet 1 to check for existing URLs/names
    url_s1 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist"
    r1 = requests.get(url_s1)
    s1_rows = list(csv.reader(io.StringIO(r1.text)))[1:]
    s1_urls = set(r[1].strip() for r in s1_rows if len(r) > 1)
    s1_names = set(r[0].strip().lower() for r in s1_rows if len(r) > 0)

    # Fetch Sheet 2
    url_s2 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2"
    r2 = requests.get(url_s2)
    s2_rows = list(csv.reader(io.StringIO(r2.text)))[1:]

    print(f"Loaded {len(s2_rows)} rows from Sheet 2.")
    print("Testing transformation: https://cdn-*.pishow.tv/live/{id}/master.m3u8 -> https://cdn.pishow.tv/ott/live/{id}/master.m3u8\n")

    results = []
    
    for r in s2_rows:
        orig_url = r[1].strip()
        name = r[0].strip()
        
        # Check if it matches cdn-*.pishow.tv/live/{id}/master.m3u8
        m = re.search(r'cdn-\d+\.pishow\.tv/live/(\d+)/master\.m3u8', orig_url)
        if not m:
            m = re.search(r'cdn\.pishow\.tv/live/(\d+)/master\.m3u8', orig_url)
        
        if m:
            stream_id = m.group(1)
            # Transformed URL
            new_url = f"https://cdn.pishow.tv/ott/live/{stream_id}/master.m3u8"
            
            # Test new URL
            is_live, code, msg = test_url(new_url)
            
            in_s1_url = new_url in s1_urls
            in_s1_name = name.lower() in s1_names
            
            results.append({
                "name": name,
                "stream_id": stream_id,
                "orig_url": orig_url,
                "new_url": new_url,
                "is_live": is_live,
                "code": code,
                "msg": msg,
                "in_s1_url": in_s1_url,
                "in_s1_name": in_s1_name,
                "orig_row": r
            })
            status_icon = "🟢 LIVE" if is_live else f"🔴 DEAD ({code})"
            s1_note = " (Already in Sheet 1!)" if in_s1_url else (" (Name matches Sheet 1)" if in_s1_name else " [NEW CHANNEL]")
            print(f"{name:<25} (ID {stream_id:>4}) -> {status_icon}{s1_note}")
            print(f"   Original: {orig_url}")
            print(f"   New URL:  {new_url}\n")

    live_count = sum(1 for res in results if res["is_live"])
    dead_count = sum(1 for res in results if not res["is_live"])
    print("==================================================")
    print(f"RESULTS: {len(results)} pishow streams tested")
    print(f"  🟢 Newly LIVE with new URL: {live_count}")
    print(f"  🔴 Still DEAD: {dead_count}")
    print("==================================================")

if __name__ == "__main__":
    main()
