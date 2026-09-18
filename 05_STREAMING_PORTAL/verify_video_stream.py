import json
import time
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Stream Playback Verifier</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body style="background:#111; color:#fff;">
    <div id="videoContainer"></div>
    <script>
        window.testStream = function(testId, streamUrl, timeoutMs) {
            return new Promise((resolve) => {
                const container = document.getElementById('videoContainer');
                const video = document.createElement('video');
                video.id = 'video_' + testId;
                video.muted = true;
                video.playsInline = true;
                video.style.width = '240px';
                video.style.height = '135px';
                container.appendChild(video);

                let hls = null;
                let resolved = false;
                let fatalError = null;

                function cleanup(result) {
                    if (resolved) return;
                    resolved = true;
                    clearInterval(pollInterval);
                    clearTimeout(timer);
                    if (hls) {
                        try { hls.destroy(); } catch(e) {}
                    }
                    try { video.pause(); video.src = ''; video.remove(); } catch(e) {}
                    resolve(result);
                }

                if (Hls.isSupported()) {
                    hls = new Hls({
                        enableWorker: false,
                        manifestLoadingTimeOut: 6000,
                        manifestLoadingMaxRetry: 1,
                        levelLoadingTimeOut: 6000,
                        fragLoadingTimeOut: 6000,
                        startFragPrefetch: true
                    });

                    hls.on(Hls.Events.ERROR, function(event, data) {
                        if (data.fatal) {
                            fatalError = data.type + ': ' + data.details + (data.response ? (' HTTP ' + data.response.code) : '');
                            cleanup({
                                playing: false,
                                reason: fatalError,
                                width: 0,
                                height: 0,
                                currentTime: 0
                            });
                        }
                    });

                    hls.on(Hls.Events.MANIFEST_PARSED, function() {
                        video.play().catch(() => {});
                    });

                    hls.loadSource(streamUrl);
                    hls.attachMedia(video);
                } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                    video.src = streamUrl;
                    video.addEventListener('loadedmetadata', () => video.play().catch(() => {}));
                } else {
                    cleanup({ playing: false, reason: 'HLS not supported', width: 0, height: 0, currentTime: 0 });
                    return;
                }

                const startTime = Date.now();
                const pollInterval = setInterval(() => {
                    const elapsed = (Date.now() - startTime) / 1000;
                    const width = video.videoWidth;
                    const height = video.videoHeight;
                    const curTime = video.currentTime;

                    if (width > 0 && height > 0 && curTime > 0.1) {
                        cleanup({
                            playing: true,
                            reason: 'Video frames actively playing',
                            width: width,
                            height: height,
                            currentTime: Math.round(curTime * 10) / 10,
                            elapsedSeconds: Math.round(elapsed * 10) / 10
                        });
                    }
                }, 200);

                const timer = setTimeout(() => {
                    cleanup({
                        playing: false,
                        reason: fatalError || 'Timeout: Video did not decode frames within ' + (timeoutMs/1000) + 's',
                        width: video.videoWidth || 0,
                        height: video.videoHeight || 0,
                        currentTime: video.currentTime || 0
                    });
                }, timeoutMs);
            });
        };
    </script>
</body>
</html>
"""

def main():
    harness_path = os.path.abspath("05_STREAMING_PORTAL/verifier_harness.html")
    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)

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

    test_urls = [
        ("IBC Tamil", "https://ibc.massstream.net/IBC/index.m3u8"),
        ("Aaryaa Tv", "https://stream.ottlive.co.in/aryatvtamil/index.m3u8"),
        ("Movie Club Tv", "https://sis-global.prod.samsungtv.plus/v1/tvpprd/sc-mp2ar4ca425xo.m3u8"),
        ("DD Tamil Cloudfront", "https://d2lk5u59tns74c.cloudfront.net/out/v1/abf46b148419409d8469d7a9b0c26563/index.m3u8"),
        ("Old 7s Music (dead)", "https://cdn-3.pishow.tv/live/1257/master.m3u8")
    ]

    for idx, (name, url) in enumerate(test_urls):
        res = driver.execute_async_script(
            """
            const testId = arguments[0];
            const url = arguments[1];
            const timeout = arguments[2];
            const done = arguments[3];
            window.testStream(testId, url, timeout).then(result => done(result));
            """,
            f"test_{idx}",
            url,
            8000
        )
        print(f"#{idx+1} {name}:", res, flush=True)

    driver.quit()

if __name__ == "__main__":
    main()
