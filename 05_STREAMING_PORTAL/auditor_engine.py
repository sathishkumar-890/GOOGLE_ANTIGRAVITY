import sys
import os
import re
import time
import subprocess
import requests
import csv
import io
import json
import numpy as np
import scipy.io.wavfile as wavfile
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

AUDIO_DIR = os.path.abspath("05_STREAMING_PORTAL/audio_samples")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Unicode ranges for Indian scripts to guarantee language match
SCRIPT_RANGES = {
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Malayalam": (0x0D00, 0x0D7F),
    "Bengali": (0x0980, 0x09FF),
    "Hindi": (0x0900, 0x097F),
    "Kannada": (0x0C80, 0x0CFF),
}

LANG_CONFIG = [
    ("Tamil", "ta-IN"),
    ("English", "en-IN"),
    ("Hindi", "hi-IN"),
    ("Telugu", "te-IN"),
    ("Malayalam", "ml-IN"),
    ("Bengali", "bn-IN"),
    ("Kannada", "kn-IN"),
]

def count_script_chars(text, lang_name):
    if lang_name not in SCRIPT_RANGES:
        return 0
    start, end = SCRIPT_RANGES[lang_name]
    return sum(1 for ch in text if start <= ord(ch) <= end)

def capture_audio(stream_url, output_wav, duration=6, timeout=12):
    """Captures duration seconds of 16kHz mono PCM audio from live stream via ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-headers", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n",
        "-rw_timeout", "8000000",
        "-analyzeduration", "2000000",
        "-probesize", "1000000",
        "-i", stream_url,
        "-t", str(duration),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_wav
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=timeout)
        if res.returncode == 0 and os.path.exists(output_wav) and os.path.getsize(output_wav) > 10000:
            return True, "Captured"
        err_msg = res.stderr.decode("utf-8", errors="ignore")[-200:]
        if "404 Not Found" in err_msg:
            return False, "404 Not Found"
        if "403 Forbidden" in err_msg:
            return False, "403 Forbidden"
        return False, f"FFmpeg failed (size={os.path.getsize(output_wav) if os.path.exists(output_wav) else 0})"
    except subprocess.TimeoutExpired:
        return False, "Timed out after 12s"
    except Exception as e:
        return False, str(e)[:60]

def analyze_audio(wav_path, hint_category=""):
    """
    Analyzes wav file for volume, speech recognition in multiple languages, or music characteristics.
    """
    try:
        sr_rate, data = wavfile.read(wav_path)
        if len(data) == 0:
            return "Dead / Silent", "", 0, "Empty audio data"

        rms = float(np.sqrt(np.mean(data.astype(np.float32)**2)))
        if rms < 35:
            return "Dead / Silent", "", rms, "RMS below audible threshold"

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        # Build language list prioritizing hint category
        prioritized_langs = []
        hint_clean = hint_category.strip().title()
        for name, code in LANG_CONFIG:
            if name == hint_clean:
                prioritized_langs.insert(0, (name, code))
            else:
                prioritized_langs.append((name, code))

        recognized_texts = {}
        for lang_name, lang_code in prioritized_langs:
            try:
                txt = recognizer.recognize_google(audio_data, language=lang_code)
                if txt and len(txt.strip()) > 0:
                    recognized_texts[lang_name] = txt.strip()
                    # If high confidence script match found for Indian language, stop early
                    if lang_name in SCRIPT_RANGES and count_script_chars(txt, lang_name) >= 3:
                        break
                    # If English matches well
                    if lang_name == "English" and len(txt.split()) >= 3 and hint_clean == "English":
                        break
            except Exception:
                pass

        if recognized_texts:
            # Score each candidate
            scores = {}
            for lang, txt in recognized_texts.items():
                if lang in SCRIPT_RANGES:
                    script_count = count_script_chars(txt, lang)
                    scores[lang] = script_count * 10 + len(txt)
                elif lang == "English":
                    # Check if purely ascii letters
                    ascii_words = len(re.findall(r'[a-zA-Z]+', txt))
                    scores[lang] = ascii_words * 5 + len(txt)
                else:
                    scores[lang] = len(txt)
            best_lang = max(scores.keys(), key=lambda k: scores[k])
            return best_lang, recognized_texts[best_lang], rms, f"Spoken speech identified ({best_lang})"

        # If speech recognition returned nothing:
        # Check music features
        # Zero-crossing rate
        zcr = float(np.mean(np.abs(np.diff(np.sign(data.astype(np.float32)))))) / 2.0
        return "Music", "", rms, f"Continuous music / instrumental track (RMS={rms:.1f}, ZCR={zcr:.4f})"

    except Exception as e:
        return "Unknown", "", 0, str(e)[:60]

def audit_stream_worker(task):
    idx, sheet_name, name, url, old_cat, old_status = task
    slug = re.sub(r'[^a-zA-Z0-9_]+', '_', name.lower()).strip('_')
    wav_path = os.path.join(AUDIO_DIR, f"{sheet_name}_{idx:02d}_{slug}.wav")

    # If stream was explicitly marked Dead and was an old defunct URL
    if old_status.strip().lower() == "dead" and ("dailyhunt" in url or "light-ott" in url or "livebox" in url):
        return {
            "index": idx,
            "sheet": sheet_name,
            "name": name,
            "url": url,
            "old_cat": old_cat,
            "new_status": "Dead",
            "detected_category": old_cat,
            "transcript": "",
            "rms": 0,
            "notes": "Defunct dead URL"
        }

    # Attempt capture
    success, capture_msg = capture_audio(url, wav_path, duration=6, timeout=12)
    if not success:
        # Try once more with duration=4
        time.sleep(0.5)
        success, capture_msg = capture_audio(url, wav_path, duration=4, timeout=10)

    if not success:
        return {
            "index": idx,
            "sheet": sheet_name,
            "name": name,
            "url": url,
            "old_cat": old_cat,
            "new_status": "Dead",
            "detected_category": old_cat,
            "transcript": "",
            "rms": 0,
            "notes": capture_msg
        }

    detected_cat, transcript, rms, notes = analyze_audio(wav_path, hint_category=old_cat)
    return {
        "index": idx,
        "sheet": sheet_name,
        "name": name,
        "url": url,
        "old_cat": old_cat,
        "new_status": "Live",
        "detected_category": detected_cat,
        "transcript": transcript,
        "rms": rms,
        "notes": notes,
        "wav": wav_path
    }

def main():
    print("==================================================================")
    print("FULL AUDIO ACOUSTIC & LANGUAGE AUDIT: SHEET 1 & SHEET 2")
    print("==================================================================")

    url_s1 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist"
    s1_rows = list(csv.reader(io.StringIO(requests.get(url_s1).text)))[1:]

    url_s2 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2"
    s2_rows = list(csv.reader(io.StringIO(requests.get(url_s2).text)))[1:]

    tasks = []
    for i, r in enumerate(s1_rows, 1):
        if r and any(r[:2]):
            tasks.append((i, "Sheet1", r[0], r[1], r[2] if len(r)>2 else "", r[4] if len(r)>4 else ""))
    for i, r in enumerate(s2_rows, 1):
        if r and any(r[:2]):
            tasks.append((i, "Sheet2", r[0], r[1], r[2] if len(r)>2 else "", r[4] if len(r)>4 else ""))

    total = len(tasks)
    print(f"Total streams queued for acoustic analysis: {total} ({len(s1_rows)} in Sheet 1, {len(s2_rows)} in Sheet 2)")

    results = []
    # 3 worker threads for optimal ffmpeg network stability without socket collision
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_task = {executor.submit(audit_stream_worker, t): t for t in tasks}
        done_count = 0
        for future in as_completed(future_to_task):
            t = future_to_task[future]
            try:
                res = future.result()
                results.append(res)
                t_snip = f" | Spoken: '{res['transcript'][:30]}...'" if res['transcript'] else f" ({res['notes']})"
                print(f"[{done_count+1:3d}/{total:3d}] [{res['sheet']:<6}] [{res['new_status']:<4}] [{res['detected_category']:<10}] {res['name']:<22}{t_snip}")
            except Exception as e:
                print(f"[{done_count+1:3d}/{total:3d}] [{t[1]:<6}] ERROR: {t[2]} -> {e}")
                results.append({
                    "index": t[0],
                    "sheet": t[1],
                    "name": t[2],
                    "url": t[3],
                    "old_cat": t[4],
                    "new_status": "Dead",
                    "detected_category": t[4],
                    "transcript": "",
                    "rms": 0,
                    "notes": str(e)
                })
            done_count += 1

    # Sort results by sheet and index
    results.sort(key=lambda x: (x["sheet"], x["index"]))

    # Save to JSON
    json_path = "05_STREAMING_PORTAL/auditor_engine_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nAudit complete! Results saved to {json_path}")

if __name__ == "__main__":
    main()
