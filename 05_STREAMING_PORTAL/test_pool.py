import json
import os
import sys
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HTML_POOL = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Stream Playback Verifier Pool</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body style="background:#0b0e14; color:#fff; font-family:sans-serif;">
    <h3>Active Video Decoder Verification Pool</h3>
    <div id="slots" style="display:flex; gap:12px; margin-bottom:16px;"></div>
    <div id="logs" style="font-family:monospace; font-size:12px; height:300px; overflow-y:auto; background:#161b22; padding:8px;"></div>
    <script>
        function log(msg) {
            const l = document.getElementById('logs');
            l.textContent += msg + "\\n";
            l.scrollTop = l.scrollHeight;
        }

        window.testSingleChannel = function(ch, slotIndex, timeoutMs) {
            return new Promise((resolve) => {
                const slots = document.getElementById('slots');
                let slot = document.getElementById('slot_' + slotIndex);
                if (!slot) {
                    slot = document.createElement('div');
                    slot.id = 'slot_' + slotIndex;
                    slot.style.border = '1px solid #30363d';
                    slot.style.padding = '6px';
                    slot.style.borderRadius = '6px';
                    slots.appendChild(slot);
                }
                slot.innerHTML = '<div style="font-size:11px; margin-bottom:4px;"><b>Slot ' + slotIndex + ':</b> #' + ch.row + ' ' + ch.name + '</div>';

                const video = document.createElement('video');
                video.muted = true;
                video.playsInline = true;
                video.autoplay = true;
                video.style.width = '200px';
                video.style.height = '112px';
                video.style.background = '#000';
                slot.appendChild(video);

                let hls = null;
                let resolved = false;
                let fatalReason = null;

                function cleanup(result) {
                    if (resolved) return;
                    resolved = true;
                    clearInterval(checkInterval);
                    clearTimeout(timeoutTimer);
                    if (hls) {
                        try { hls.destroy(); } catch(e) {}
                    }
                    try {
                        video.pause();
                        video.src = '';
                        video.remove();
                    } catch(e) {}
                    resolve(result);
                }

                if (Hls.isSupported()) {
                    hls = new Hls({
                        enableWorker: false,
                        manifestLoadingTimeOut: 6000,
                        manifestLoadingMaxRetry: 1,
                        levelLoadingTimeOut: 6000,
                        levelLoadingMaxRetry: 1,
                        fragLoadingTimeOut: 6000,
                        fragLoadingMaxRetry: 1,
                        startFragPrefetch: true
                    });

                    hls.on(Hls.Events.ERROR, function(event, data) {
                        if (data.fatal) {
                            fatalReason = (data.details || data.type) + (data.response ? (' HTTP ' + data.response.code) : '');
                            cleanup({
                                row: ch.row,
                                name: ch.name,
                                url: ch.url,
                                playing: false,
                                reason: fatalReason,
                                resolution: '0x0',
                                currentTime: 0
                            });
                        }
                    });

                    hls.on(Hls.Events.MANIFEST_PARSED, function() {
                        video.play().catch(() => {});
                    });

                    hls.loadSource(ch.url);
                    hls.attachMedia(video);
                } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                    video.src = ch.url;
                    video.addEventListener('loadedmetadata', () => video.play().catch(() => {}));
                } else {
                    cleanup({
                        row: ch.row,
                        name: ch.name,
                        url: ch.url,
                        playing: false,
                        reason: 'HLS not supported',
                        resolution: '0x0',
                        currentTime: 0
                    });
                    return;
                }

                const startTime = Date.now();
                const checkInterval = setInterval(() => {
                    const elapsed = (Date.now() - startTime) / 1000;
                    const w = video.videoWidth;
                    const h = video.videoHeight;
                    const ct = video.currentTime;

                    // STRICT VIDEO PLAYING VERIFICATION:
                    // Both width and height must be > 0 (decoded video frame)
                    // and currentTime must be advancing
                    if (w > 0 && h > 0 && ct > 0.05) {
                        cleanup({
                            row: ch.row,
                            name: ch.name,
                            url: ch.url,
                            playing: true,
                            reason: 'Video frames actively playing',
                            resolution: w + 'x' + h,
                            currentTime: Math.round(ct * 10) / 10,
                            elapsedSeconds: Math.round(elapsed * 10) / 10
                        });
                    }
                }, 150);

                const timeoutTimer = setTimeout(() => {
                    cleanup({
                        row: ch.row,
                        name: ch.name,
                        url: ch.url,
                        playing: false,
                        reason: fatalReason || 'Timeout: No video frames decoded within ' + (timeoutMs/1000) + 's',
                        resolution: (video.videoWidth || 0) + 'x' + (video.videoHeight || 0),
                        currentTime: Math.round((video.currentTime || 0) * 10) / 10
                    });
                }, timeoutMs);
            });
        };

        // Worker pool of size N
        window.runPool = async function(channelList, concurrency, timeoutMs) {
            const results = new Array(channelList.length);
            let nextIndex = 0;

            async function worker(workerId) {
                while (nextIndex < channelList.length) {
                    const currentIdx = nextIndex++;
                    const ch = channelList[currentIdx];
                    const res = await window.testSingleChannel(ch, workerId, timeoutMs);
                    results[currentIdx] = res;
                }
            }

            const workers = [];
            for (let i = 0; i < concurrency; i++) {
                workers.push(worker(i + 1));
            }
            await Promise.all(workers);
            return results;
        };
    </script>
</body>
</html>
"""

def main():
    harness_path = os.path.abspath("05_STREAMING_PORTAL/pool_harness.html")
    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(HTML_POOL)

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

    test_channels = [
        {"row": 2, "name": "7s Music Tv (old)", "url": "https://cdn-3.pishow.tv/live/1257/master.m3u8"},
        {"row": 3, "name": "Aaryaa Tv", "url": "https://stream.ottlive.co.in/aryatvtamil/index.m3u8"},
        {"row": 6, "name": "Fail Army", "url": "https://failarmy-international-in.samsung.wurl.tv/playlist.m3u8"},
        {"row": 9, "name": "Isaiaruvi Tv", "url": "https://segment.yuppcdn.net/140622/isaiaruvi/playlist.m3u8"},
        {"row": 10, "name": "Kalaignar Tv", "url": "https://segment.yuppcdn.net/240122/kalaignartv/playlist.m3u8"},
        {"row": 15, "name": "MN Tv", "url": "https://mntv.livebox.co.in/mntvhls/live.m3u8"},
        {"row": 17, "name": "Movie Club 2 Tv", "url": "https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf"},
        {"row": 18, "name": "Movie Club Tv", "url": "https://sis-global.prod.samsungtv.plus/v1/tvpprd/sc-mp2ar4ca425xo.m3u8"},
        {"row": 28, "name": "Rakuten Action Movies", "url": "https://54045f0c40fd442c8b06df076aaf1e85.mediatailor.eu-west-1.amazonaws.com/v1/master/0547f18649bd788bec7b67b746e47670f558b6b2/production-LiveChannel-6065/master.m3u8"},
        {"row": 60, "name": "Win Tv (old)", "url": "https://cdn-4.pishow.tv/live/1531/master.m3u8"}
    ]

    print("Running pool test on 10 channels with concurrency=2...")
    t0 = time.time()
    results = driver.execute_async_script(
        """
        const chs = arguments[0];
        const concurrency = arguments[1];
        const timeout = arguments[2];
        const done = arguments[3];
        window.runPool(chs, concurrency, timeout).then(res => done(res));
        """,
        test_channels,
        2,
        7000
    )
    elapsed = time.time() - t0

    print(f"\nPool completed in {elapsed:.1f}s:")
    for r in results:
        status_tag = "[PLAYING]" if r["playing"] else "[OFFLINE]"
        res_str = f"[{r['resolution']}]" if r["playing"] else ""
        print(f"Row {r['row']:2d} | {status_tag:10s} {res_str:10s} | {r['name']:25s} | {r['reason']}")

    driver.quit()

if __name__ == "__main__":
    main()
