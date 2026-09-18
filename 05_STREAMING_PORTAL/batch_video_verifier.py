import csv
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

# HTML Harness supporting concurrent multi-video playback verification
HTML_HARNESS = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Parallel Stream Playback Verifier</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body style="background:#0a0a0f; color:#eee; font-family:sans-serif;">
    <h3>Active Video Playback Test Chamber</h3>
    <div id="videoGrid" style="display:flex; flex-wrap:wrap; gap:8px;"></div>
    <script>
        window.testSingleChannel = function(ch, timeoutMs) {
            return new Promise((resolve) => {
                const grid = document.getElementById('videoGrid');
                const box = document.createElement('div');
                box.style.border = '1px solid #333';
                box.style.padding = '4px';
                box.id = 'box_' + ch.id;

                const label = document.createElement('div');
                label.style.fontSize = '10px';
                label.textContent = '#' + ch.row + ' ' + ch.name;
                box.appendChild(label);

                const video = document.createElement('video');
                video.muted = true;
                video.playsInline = true;
                video.style.width = '120px';
                video.style.height = '68px';
                video.style.background = '#000';
                box.appendChild(video);
                grid.appendChild(box);

                let hls = null;
                let resolved = false;
                let fatalReason = null;

                function finish(result) {
                    if (resolved) return;
                    resolved = true;
                    clearInterval(checker);
                    clearTimeout(timer);
                    if (hls) {
                        try { hls.destroy(); } catch(e) {}
                    }
                    try { video.pause(); video.src = ''; box.remove(); } catch(e) {}
                    resolve(result);
                }

                if (Hls.isSupported()) {
                    hls = new Hls({
                        enableWorker: false,
                        manifestLoadingTimeOut: 5000,
                        manifestLoadingMaxRetry: 0,
                        levelLoadingTimeOut: 5000,
                        levelLoadingMaxRetry: 0,
                        fragLoadingTimeOut: 5000,
                        fragLoadingMaxRetry: 0,
                        startFragPrefetch: true
                    });

                    hls.on(Hls.Events.ERROR, function(event, data) {
                        if (data.fatal) {
                            fatalReason = (data.details || data.type) + (data.response ? (' ' + data.response.code) : '');
                            finish({
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
                    finish({
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
                const checker = setInterval(() => {
                    const elapsed = (Date.now() - startTime) / 1000;
                    const w = video.videoWidth;
                    const h = video.videoHeight;
                    const ct = video.currentTime;

                    // STRICT VIDEO PLAYBACK CRITERION:
                    // 1. Decoded video width > 0 and height > 0
                    // 2. Playback progress currentTime > 0.1s
                    // 3. Not paused, active frame decoding
                    if (w > 0 && h > 0 && ct > 0.1) {
                        finish({
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

                const timer = setTimeout(() => {
                    finish({
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

        window.testBatch = function(channels, timeoutMs) {
            return Promise.all(channels.map(ch => window.testSingleChannel(ch, timeoutMs)));
        };
    </script>
</body>
</html>
"""

def parse_sheet_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        all_rows = list(reader)

    channels = []
    for idx, r in enumerate(all_rows):
        if not r or len(r) < 2:
            continue
        name = r[0].strip()
        url = r[1].strip()
        if name.upper() == "STREAM NAME" or not url.startswith("http"):
            continue
        cat = r[2].strip() if len(r) > 2 else ""
        icon = r[3].strip() if len(r) > 3 else ""
        status = r[4].strip() if len(r) > 4 else ""
        channels.append({
            "id": f"row_{idx+1}",
            "row": idx + 1,
            "raw_row_idx": idx,
            "name": name,
            "url": url,
            "cat": cat,
            "icon": icon,
            "orig_status": status
        })

    return all_rows, channels

def run_batch_verification():
    csv_path = os.path.abspath("05_STREAMING_PORTAL/current_google_sheet.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist!")
        sys.exit(1)

    raw_rows, channels = parse_sheet_csv(csv_path)
    total_channels = len(channels)
    print(f"Loaded {total_channels} channels from Google Sheet CSV.")

    harness_path = os.path.abspath("05_STREAMING_PORTAL/batch_harness.html")
    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(HTML_HARNESS)

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

    BATCH_SIZE = 8
    TIMEOUT_MS = 6000
    results = []

    print(f"\nStarting batch verification: {total_channels} streams in batches of {BATCH_SIZE}...")
    start_total_time = time.time()

    for i in range(0, total_channels, BATCH_SIZE):
        batch = channels[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total_channels + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"\n--- Batch {batch_num}/{total_batches} (Channels {i+1} to {min(i+BATCH_SIZE, total_channels)}) ---", flush=True)

        batch_start = time.time()
        batch_results = driver.execute_async_script(
            """
            const chs = arguments[0];
            const timeout = arguments[1];
            const done = arguments[2];
            window.testBatch(chs, timeout).then(res => done(res));
            """,
            batch,
            TIMEOUT_MS
        )
        for r in batch_results:
            status_icon = "[PLAYING]" if r["playing"] else "[OFFLINE]"
            res_str = f"[{r['resolution']}]" if r["playing"] else ""
            name_clean = r['name'][:25].encode('ascii', errors='replace').decode('ascii')
            print(f"Row {r['row']:3d} | {status_icon:10s} {res_str:10s} | {name_clean:25s} | {r['reason']}", flush=True)
            results.append(r)

    driver.quit()
    total_time = time.time() - start_total_time

    playing_count = sum(1 for r in results if r["playing"])
    offline_count = sum(1 for r in results if not r["playing"])
    print(f"\n=======================================================", flush=True)
    print(f"VERIFICATION COMPLETE in {total_time:.1f}s", flush=True)
    print(f"[+] Actively Playing: {playing_count}", flush=True)
    print(f"[-] Not Playing / Offline: {offline_count}", flush=True)
    print(f"=======================================================\n", flush=True)

    # Save detailed JSON verification log
    json_path = os.path.abspath("05_STREAMING_PORTAL/verification_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved detailed results to {json_path}")

    # Build updated rows for Google Sheet CSV
    row_result_map = {r["row"]: r for r in results}
    updated_rows = []
    for idx, r in enumerate(raw_rows):
        row_num = idx + 1
        if row_num in row_result_map:
            res = row_result_map[row_num]
            new_status = "Playing" if res["playing"] else "Not Playing"
            # Ensure row has at least 5 columns
            while len(r) < 5:
                r.append("")
            r[4] = new_status
            updated_rows.append(r)
        else:
            updated_rows.append(r)

    # Write updated Google Sheet CSV
    updated_csv_path = os.path.abspath("05_STREAMING_PORTAL/Google_Sheet_Updated_Status.csv")
    with open(updated_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)
    print(f"Generated updated CSV: {updated_csv_path}")

    # Also generate formatted Excel with openpyxl
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "IPTV Stream Status"

        header_fill = PatternFill(start_color="1A1D20", end_color="1A1D20", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        sub_header_fill = PatternFill(start_color="2D3748", end_color="2D3748", fill_type="solid")

        playing_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
        playing_font = Font(name="Calibri", size=10, bold=True, color="155724")

        offline_fill = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
        offline_font = Font(name="Calibri", size=10, bold=True, color="721C24")

        thin_border = Border(
            left=Side(style='thin', color='E2E8F0'),
            right=Side(style='thin', color='E2E8F0'),
            top=Side(style='thin', color='E2E8F0'),
            bottom=Side(style='thin', color='E2E8F0')
        )

        for row_idx, r in enumerate(updated_rows, start=1):
            for col_idx, val in enumerate(r, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                if row_idx == 1 or (len(r) > 0 and r[0].strip().upper() == "STREAM NAME"):
                    cell.fill = header_fill if row_idx == 1 else sub_header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                elif col_idx == 5:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    if str(val).strip() == "Playing":
                        cell.fill = playing_fill
                        cell.font = playing_font
                    elif str(val).strip() == "Not Playing":
                        cell.fill = offline_fill
                        cell.font = offline_font

        # Adjust column widths
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = max(len(str(cell.value or '')) for cell in col)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        excel_path = os.path.abspath("05_STREAMING_PORTAL/Google_Sheet_Updated_Status.xlsx")
        wb.save(excel_path)
        print(f"Generated formatted Excel: {excel_path}")
    except Exception as e:
        print(f"Excel generation note: {e}")

if __name__ == "__main__":
    run_batch_verification()
