import os
import sys
import time
import json
import requests
import csv
import io
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding="utf-8")

def get_all_unique_streams():
    headers = {"User-Agent": "Mozilla/5.0"}
    all_streams = {}

    # 1. Fetch Sheet 1 from Google Sheets
    try:
        r1 = requests.get(
            "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist",
            headers=headers, timeout=12
        )
        s1 = list(csv.reader(io.StringIO(r1.text)))
        for r in s1[1:]:
            if r and len(r) >= 2 and r[1].startswith("http"):
                url = r[1].strip()
                name = r[0].strip()
                cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
                icon = r[3].strip() if len(r) > 3 and r[3].strip() else "📺"
                all_streams[url] = {"name": name, "url": url, "cat": cat, "icon": icon, "origin": "Sheet1"}
    except Exception as e:
        print(f"Warn: Sheet1 online fetch failed: {e}")

    # 2. Fetch Sheet 2 from Google Sheets
    try:
        r2 = requests.get(
            "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2",
            headers=headers, timeout=12
        )
        s2 = list(csv.reader(io.StringIO(r2.text)))
        for r in s2[1:]:
            if r and len(r) >= 2 and r[1].startswith("http"):
                url = r[1].strip()
                name = r[0].strip()
                cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
                icon = r[3].strip() if len(r) > 3 and r[3].strip() else "📺"
                if url not in all_streams:
                    all_streams[url] = {"name": name, "url": url, "cat": cat, "icon": icon, "origin": "Sheet2"}
    except Exception as e:
        print(f"Warn: Sheet2 online fetch failed: {e}")

    # 3. Also read local CSVs to ensure zero missing channels
    for f, origin in [("Sheet1_Merged_Final.csv", "Local_S1"), ("Sheet2_Dead_Only.csv", "Local_S2")]:
        p = os.path.join("05_STREAMING_PORTAL", f)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fp:
                rows = list(csv.reader(fp))
                for r in rows[1:]:
                    if r and len(r) >= 2 and r[1].startswith("http"):
                        url = r[1].strip()
                        name = r[0].strip()
                        cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
                        icon = r[3].strip() if len(r) > 3 and r[3].strip() else "📺"
                        if url not in all_streams:
                            all_streams[url] = {"name": name, "url": url, "cat": cat, "icon": icon, "origin": origin}

    return list(all_streams.values())

def main():
    streams = get_all_unique_streams()
    print("==========================================================================")
    print(f"TOTAL UNIQUE STREAMS TO TEST IN WEB APP: {len(streams)}")
    print("==========================================================================")

    temp_dir = tempfile.mkdtemp()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("\nLogging into PythonAnywhere Web App...")
        driver.get("https://sathishkumar890.pythonanywhere.com/")
        u = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        u.clear()
        u.send_keys("USER")
        p = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        p.clear()
        p.send_keys("123456789")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.url_contains("/streams/content_page/"))
        print("Logged in successfully! On /streams/content_page/\n")

        # Inject helper testing function into window
        driver.execute_script("""
            window.__testResults = {};
            window.testStreamInWebApp = function(streamUrl) {
                return new Promise((resolve) => {
                    const video = document.getElementById('players');
                    if (!video) return resolve({ ok: false, error: 'no video element' });
                    
                    if (window.__testHls) {
                        try { window.__testHls.destroy(); } catch(e) {}
                        window.__testHls = null;
                    }
                    
                    video.pause();
                    video.removeAttribute('src');
                    video.load();

                    let hasResolved = false;
                    let lastError = null;

                    const timer = setTimeout(() => {
                        if (!hasResolved) {
                            hasResolved = true;
                            const isPlaying = (video.videoWidth > 0 && video.currentTime > 0.1 && video.readyState >= 2);
                            resolve({
                                ok: isPlaying,
                                videoWidth: video.videoWidth || 0,
                                videoHeight: video.videoHeight || 0,
                                currentTime: video.currentTime || 0,
                                readyState: video.readyState || 0,
                                error: isPlaying ? null : (lastError || 'timeout - no video frames')
                            });
                        }
                    }, 5000);

                    const checker = setInterval(() => {
                        if (video.videoWidth > 0 && video.currentTime > 0.2 && video.readyState >= 2) {
                            if (!hasResolved) {
                                hasResolved = true;
                                clearInterval(checker);
                                clearTimeout(timer);
                                resolve({
                                    ok: true,
                                    videoWidth: video.videoWidth,
                                    videoHeight: video.videoHeight,
                                    currentTime: video.currentTime,
                                    readyState: video.readyState,
                                    error: null
                                });
                            }
                        }
                    }, 250);

                    if (Hls.isSupported()) {
                        const hls = new Hls({
                            enableWorker: false,
                            lowLatencyMode: true,
                            manifestLoadingTimeOut: 4000,
                            manifestLoadingMaxRetry: 1,
                            levelLoadingTimeOut: 4000,
                            levelLoadingMaxRetry: 1,
                            fragLoadingTimeOut: 4000,
                            fragLoadingMaxRetry: 1
                        });
                        window.__testHls = hls;

                        hls.on(Hls.Events.ERROR, (event, data) => {
                            lastError = `${data.type} (${data.details})`;
                            if (data.fatal) {
                                if (!hasResolved) {
                                    hasResolved = true;
                                    clearInterval(checker);
                                    clearTimeout(timer);
                                    try { hls.destroy(); } catch(e) {}
                                    resolve({
                                        ok: false,
                                        videoWidth: 0,
                                        videoHeight: 0,
                                        currentTime: 0,
                                        readyState: video.readyState || 0,
                                        error: `Fatal HLS: ${data.details}`
                                    });
                                }
                            }
                        });

                        hls.loadSource(streamUrl);
                        hls.attachMedia(video);
                        video.play().catch(e => {
                            lastError = `Play rejected: ${e.message}`;
                        });
                    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                        video.src = streamUrl;
                        video.play().catch(e => {
                            lastError = `Native play error: ${e.message}`;
                        });
                    } else {
                        clearTimeout(timer);
                        clearInterval(checker);
                        resolve({ ok: false, error: 'HLS not supported' });
                    }
                });
            };
        """)

        results = []
        live_count = 0
        dead_count = 0

        print(f"{'#':<3} | {'STATUS':<7} | {'CHANNEL NAME':<26} | {'RESOLUTION':<11} | {'DIAGNOSTIC'}")
        print("-" * 80)

        for idx, item in enumerate(streams, 1):
            url = item["url"]
            name = item["name"]

            # Run test inside web app
            res = driver.execute_async_script("""
                const url = arguments[0];
                const callback = arguments[arguments.length - 1];
                window.testStreamInWebApp(url).then(callback);
            """, url)

            is_ok = res.get("ok", False)
            dim = f"{res.get('videoWidth', 0)}x{res.get('videoHeight', 0)}" if is_ok else "-"
            err = res.get("error") or "OK"

            if is_ok:
                status = "Live"
                live_count += 1
                status_badge = "[LIVE]"
            else:
                status = "Dead"
                dead_count += 1
                status_badge = "[DEAD]"

            print(f"{idx:2d}  | {status_badge:<7} | {name:<26} | {dim:<11} | {err}")

            item["status"] = status
            item["web_ok"] = is_ok
            item["resolution"] = dim
            item["diagnostic"] = err
            results.append(item)

        print("\n" + "=" * 80)
        print(f"WEB APP IN-BROWSER TEST FINISHED: {live_count} LIVE (Plays in Web App), {dead_count} DEAD / UNPLAYABLE")
        print("=" * 80)

        out_json = "05_STREAMING_PORTAL/webapp_stream_test_results.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Saved audit results to: {out_json}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
