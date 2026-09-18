import json
import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HTML_DEBUG = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body style="background:#111; color:#fff;">
    <video id="v" muted playsinline autoplay style="width:320px;height:180px;"></video>
    <div id="logs" style="font-family:monospace; font-size:11px; white-space:pre-wrap;"></div>
    <script>
        const v = document.getElementById('v');
        const l = document.getElementById('logs');
        function log(msg) {
            console.log(msg);
            l.textContent += msg + "\\n";
        }

        window.testUrl = function(url) {
            return new Promise((resolve) => {
                log('Loading: ' + url);
                const hls = new Hls({ enableWorker: false });
                hls.on(Hls.Events.ERROR, (e, d) => {
                    log('HLS ERROR: fatal=' + d.fatal + ', type=' + d.type + ', details=' + d.details + ', code=' + (d.response ? d.response.code : 'none'));
                    if (d.fatal) {
                        resolve({ success: false, reason: d.details });
                    }
                });
                hls.on(Hls.Events.MANIFEST_LOADED, (e, d) => log('MANIFEST LOADED! levels=' + d.levels.length));
                hls.on(Hls.Events.MANIFEST_PARSED, (e, d) => {
                    log('MANIFEST PARSED! levels=' + d.levels.length);
                    v.play().catch(err => log('Play err: ' + err));
                });
                hls.on(Hls.Events.FRAG_LOADED, (e, d) => log('FRAG LOADED: ' + d.frag.sn));

                v.addEventListener('playing', () => log('EVENT: playing'));
                v.addEventListener('timeupdate', () => {
                    log('EVENT: timeupdate w=' + v.videoWidth + ' h=' + v.videoHeight + ' t=' + v.currentTime);
                    if (v.videoWidth > 0 && v.currentTime > 0.1) {
                        resolve({ success: true, width: v.videoWidth, height: v.videoHeight, time: v.currentTime });
                    }
                });

                hls.loadSource(url);
                hls.attachMedia(v);

                setTimeout(() => {
                    resolve({ success: false, reason: 'timeout 8s', w: v.videoWidth, t: v.currentTime });
                }, 8000);
            });
        };
    </script>
</body>
</html>
"""

def main():
    harness_path = os.path.abspath("05_STREAMING_PORTAL/debug_harness.html")
    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(HTML_DEBUG)

    temp_dir = tempfile.mkdtemp()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    driver = webdriver.Chrome(options=options)
    driver.get(f"file:///{harness_path.replace(os.sep, '/')}")
    time.sleep(1)

    url = "https://54045f0c40fd442c8b06df076aaf1e85.mediatailor.eu-west-1.amazonaws.com/v1/master/0547f18649bd788bec7b67b746e47670f558b6b2/production-LiveChannel-6065/master.m3u8"
    res = driver.execute_async_script(
        """
        const url = arguments[0];
        const done = arguments[1];
        window.testUrl(url).then(r => done(r));
        """,
        url
    )
    print("Result:", res)

    logs = driver.find_element("id", "logs").text
    print("\nLogs:\n", logs)

    driver.quit()

if __name__ == "__main__":
    main()
