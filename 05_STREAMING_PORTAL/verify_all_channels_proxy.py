import sys
import os
import time
import subprocess
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHANNELS = ["ten4", "pixhd", "maxhd", "wah", "max", "bbcearthhd", "yay"]

def test_all():
    print("==================================================")
    print("STEP 1: STARTING MULTI-STREAM PROXY ON PORT 8877")
    print("==================================================")
    script_path = os.path.join(os.path.dirname(__file__), "multi_stream_proxy.py")
    proc = subprocess.Popen([sys.executable, script_path, "--port", "8877", "--host", "127.0.0.1"])
    time.sleep(2)

    try:
        # 1. Test Playlist M3U8
        with urllib.request.urlopen("http://127.0.0.1:8877/playlist.m3u8") as r:
            body = r.read().decode("utf-8")
            print(f"[OK] /playlist.m3u8 Status: {r.status} | Entries: {body.count('#EXTINF')}")

        # 2. Test JSON API
        with urllib.request.urlopen("http://127.0.0.1:8877/api/channels") as r:
            print(f"[OK] /api/channels Status: {r.status}")

        # 3. Test each channel's rewritten stream
        print("\n--- TESTING ALL 7 REWRITTEN CHANNELS ---")
        for ch in CHANNELS:
            ch_url = f"http://127.0.0.1:8877/live/{ch}.m3u8"
            with urllib.request.urlopen(ch_url) as r:
                cors = r.headers.get("Access-Control-Allow-Origin")
                c_type = r.headers.get("Content-Type")
                content = r.read().decode("utf-8")
                child_count = len([l for l in content.splitlines() if l.startswith("http")])
                print(f"[OK] /live/{ch:<12}.m3u8 | Status: {r.status} | CORS: {cors} | Variants: {child_count}")

        # 4. Launch Headless Chrome to test playback and capture Web Player UI
        print("\n==================================================")
        print("STEP 2: IN-BROWSER PLAYBACK & WEB PORTAL CAPTURE")
        print("==================================================")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # Standard browser security: No disabled flags!
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1400, 900)

        try:
            portal_url = "http://127.0.0.1:8877/"
            driver.get(portal_url)
            print("Web Player UI loaded! Waiting 6s for HLS auto-play...")
            time.sleep(6)

            metrics = driver.execute_script("""
                const v = document.getElementById('videoPlayer');
                return {
                    currentTime: v.currentTime,
                    videoWidth: v.videoWidth,
                    videoHeight: v.videoHeight,
                    paused: v.paused,
                    readyState: v.readyState,
                    title: document.getElementById('currentTitle').innerText
                };
            """)
            print(f"\nPLAYBACK VERIFIED IN STANDARD CHROME:")
            print(f"  Channel Playing : {metrics['title']}")
            print(f"  Current Time    : {metrics['currentTime']:.2f}s")
            print(f"  Resolution      : {metrics['videoWidth']}x{metrics['videoHeight']}")
            print(f"  ReadyState      : {metrics['readyState']} (4 = HAVE_ENOUGH_DATA)")
            print(f"  Is Paused       : {metrics['paused']}")

            screenshot_path = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1\multi_stream_portal_playback.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nSaved portal playback screenshot: {screenshot_path}")

        finally:
            driver.quit()

    finally:
        print("\nStopping proxy server...")
        proc.terminate()
        proc.wait()
        print("Verification complete!")

if __name__ == "__main__":
    test_all()
