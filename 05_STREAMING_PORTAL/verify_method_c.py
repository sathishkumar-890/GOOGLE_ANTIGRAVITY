import sys
import os
import time
import subprocess
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_verification():
    print("==================================================")
    print("STEP 1: LAUNCHING METHOD C HLS PROXY SERVER")
    print("==================================================")
    proxy_script = os.path.join(os.path.dirname(__file__), "hls_streaming_proxy.py")
    proc = subprocess.Popen([sys.executable, proxy_script, "--port", "8899", "--host", "127.0.0.1"])
    time.sleep(2)

    try:
        # Check health
        health_url = "http://127.0.0.1:8899/health"
        with urllib.request.urlopen(health_url) as r:
            print(f"Health Check Status: {r.status} - {r.read().decode('utf-8').strip()}")

        # Check rewritten M3U8
        target_stream = "https://cloudplay-sonyliv.pages.dev/ten4.m3u8"
        proxied_master = f"http://127.0.0.1:8899/proxy?url={urllib.parse.quote(target_stream)}"
        with urllib.request.urlopen(proxied_master) as r:
            cors_origin = r.headers.get("Access-Control-Allow-Origin")
            print(f"Master Playlist Status: {r.status} | CORS Header: Access-Control-Allow-Origin={cors_origin}")
            master_body = r.read().decode("utf-8")
            child_lines = [l for l in master_body.splitlines() if not l.startswith("#") and l.strip()]
            print(f"Rewritten Child Playlist Sample:\n  {child_lines[0][:100]}...\n")

        # Test fetching child playlist
        with urllib.request.urlopen(child_lines[0]) as cr:
            child_body = cr.read().decode("utf-8")
            key_line = next((l for l in child_body.splitlines() if l.startswith("#EXT-X-KEY")), None)
            print(f"Rewritten AES-128 Key Line:\n  {key_line[:110]}...\n")

        print("==================================================")
        print("STEP 2: IN-BROWSER PLAYBACK VERIFICATION (CHROME)")
        print("==================================================")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # Standard Chrome security: DO NOT disable web security! We want to prove standard browser plays it!
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1280, 720)

        test_html = f"""<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body style="margin:0;background:#000;">
  <video id="video" controls autoplay muted width="1280" height="720"></video>
  <script>
    const video = document.getElementById('video');
    const hls = new Hls();
    hls.loadSource('{proxied_master}');
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function() {{
      console.log('MANIFEST_PARSED');
      video.play();
    }});
  </script>
</body>
</html>"""

        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(test_html)
            tmp_path = f.name

        try:
            driver.get("file:///" + tmp_path.replace("\\", "/"))
            print("Loading stream in standard Chrome browser through Method C Proxy...")
            time.sleep(6)

            metrics = driver.execute_script("""
                const v = document.getElementById('video');
                return {
                    currentTime: v.currentTime,
                    videoWidth: v.videoWidth,
                    videoHeight: v.videoHeight,
                    paused: v.paused,
                    readyState: v.readyState
                };
            """)
            print(f"Playback Metrics in Standard Browser:")
            print(f"  Current Time : {metrics['currentTime']:.2f}s")
            print(f"  Resolution   : {metrics['videoWidth']}x{metrics['videoHeight']}")
            print(f"  ReadyState   : {metrics['readyState']} (4 = HAVE_ENOUGH_DATA)")
            print(f"  Is Paused    : {metrics['paused']}")

            screenshot_path = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1\method_c_live_playback.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nCaptured live playback screenshot: {screenshot_path}")

        finally:
            driver.quit()
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    finally:
        print("\nStopping proxy server...")
        proc.terminate()
        proc.wait()
        print("Done!")

if __name__ == "__main__":
    run_verification()
