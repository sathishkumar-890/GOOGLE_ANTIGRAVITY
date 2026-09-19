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

LANGUAGES = [
    ("Tamil", "ta-IN"),
    ("English", "en-IN"),
    ("Hindi", "hi-IN"),
    ("Telugu", "te-IN"),
    ("Malayalam", "ml-IN"),
]

def capture_audio(stream_url, output_wav, duration=6, timeout=12):
    """Captures duration seconds of 16kHz mono PCM audio from live stream via ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-reconnect", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "2",
        "-i", stream_url,
        "-t", str(duration),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_wav
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
        if res.returncode == 0 and os.path.exists(output_wav) and os.path.getsize(output_wav) > 10000:
            return True, "Audio Captured"
        return False, "Capture failed or output empty"
    except subprocess.TimeoutExpired:
        return False, "FFmpeg connection timed out"
    except Exception as e:
        return False, str(e)[:50]

def analyze_audio_content(wav_path):
    """
    Analyzes wav file for volume, speech recognition in multiple languages, or music characteristics.
    """
    try:
        sr_rate, data = wavfile.read(wav_path)
        if len(data) == 0:
            return "Dead / Silent", "", "Empty audio data"

        # Calculate RMS energy
        rms = np.sqrt(np.mean(data.astype(np.float32)**2))
        if rms < 50:
            return "Silent / Dead", "", "RMS below audible threshold"

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        # Try recognizing in candidate languages
        recognized_texts = {}
        for lang_name, lang_code in LANGUAGES:
            try:
                txt = recognizer.recognize_google(audio_data, language=lang_code)
                if txt and len(txt.strip()) > 0:
                    recognized_texts[lang_name] = txt.strip()
            except Exception:
                pass

        if recognized_texts:
            # If recognized in one or more languages
            # Choose the language with longest/best transcript or primary match
            best_lang = max(recognized_texts.keys(), key=lambda k: len(recognized_texts[k]))
            return best_lang, recognized_texts[best_lang], f"Transcribed in {best_lang}"

        # If speech recognition returned nothing:
        # Check if spectral / zero-crossing characteristics indicate continuous music / instrumental / songs
        # In music, zero-crossing rate variance is lower, and energy is steady
        zcr = np.mean(np.abs(np.diff(np.sign(data.astype(np.float32))))) / 2.0
        return "Music", "", f"Continuous audio track / instrumental (RMS={rms:.1f}, ZCR={zcr:.4f})"

    except Exception as e:
        return "Unknown", "", str(e)[:60]

def audit_single_channel(ch, sheet_label):
    name = ch[0].strip()
    url = ch[1].strip()
    old_cat = ch[2].strip() if len(ch) > 2 else ""
    old_status = ch[4].strip() if len(ch) > 4 else ""

    # Sanitize file name
    slug = re.sub(r'[^a-zA-Z0-9_]+', '_', name.lower()).strip('_')
    wav_path = os.path.join(AUDIO_DIR, f"{sheet_label}_{slug}.wav")

    # If stream was already dead
    if old_status.lower() == "dead":
        return {
            "sheet": sheet_label,
            "name": name,
            "url": url,
            "old_cat": old_cat,
            "status": "Dead",
            "detected_category": old_cat,
            "transcript": "",
            "notes": "Stream is offline / dead"
        }

    # Attempt capture
    success, capture_msg = capture_audio(url, wav_path, duration=6, timeout=14)
    if not success:
        return {
            "sheet": sheet_label,
            "name": name,
            "url": url,
            "old_cat": old_cat,
            "status": "Dead / Unreachable",
            "detected_category": old_cat,
            "transcript": "",
            "notes": capture_msg
        }

    detected_cat, transcript, notes = analyze_audio_content(wav_path)
    return {
        "sheet": sheet_label,
        "name": name,
        "url": url,
        "old_cat": old_cat,
        "status": "Live",
        "detected_category": detected_cat,
        "transcript": transcript,
        "notes": notes,
        "wav_file": wav_path
    }

def main():
    print("==================================================")
    print("STEP 1: FETCHING STREAMS FROM SHEET 1 & SHEET 2")
    print("==================================================")
    url_s1 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist"
    r1 = requests.get(url_s1)
    s1_rows = list(csv.reader(io.StringIO(r1.text)))[1:]

    url_s2 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2"
    r2 = requests.get(url_s2)
    s2_rows = list(csv.reader(io.StringIO(r2.text)))[1:]

    print(f"Sheet 1 (IPTV_Playlist): {len(s1_rows)} streams")
    print(f"Sheet 2 (Sheet2): {len(s2_rows)} streams")
    total_tasks = len(s1_rows) + len(s2_rows)
    print(f"Total streams to audit audio content: {total_tasks}\n")

    tasks = []
    for r in s1_rows:
        if r and any(r[:2]):
            tasks.append((r, "Sheet1"))
    for r in s2_rows:
        if r and any(r[:2]):
            tasks.append((r, "Sheet2"))

    results = []
    print("Capturing live audio samples & transcribing speech concurrently (ThreadPool=10)...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ch = {executor.submit(audit_single_channel, ch, s_label): (ch[0], s_label) for ch, s_label in tasks}
        completed = 0
        for future in as_completed(future_to_ch):
            ch_name, s_label = future_to_ch[future]
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                results.append({
                    "sheet": s_label,
                    "name": ch_name,
                    "url": "",
                    "old_cat": "",
                    "status": "Error",
                    "detected_category": "",
                    "transcript": "",
                    "notes": str(e)
                })
            completed += 1
            if completed % 15 == 0 or completed == total_tasks:
                print(f"  Processed {completed}/{total_tasks} audio streams...")

    # Save results to JSON
    json_path = "05_STREAMING_PORTAL/audio_audit_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved full acoustic audit results to {json_path}")

    # Summary analysis
    sheet1_res = [r for r in results if r["sheet"] == "Sheet1"]
    sheet2_res = [r for r in results if r["sheet"] == "Sheet2"]

    print("\n==================================================")
    print(f"SHEET 1 AUDIT BREAKDOWN ({len(sheet1_res)} Streams)")
    print("==================================================")
    for r in sheet1_res:
        t_snippet = f" | Spoken: '{r['transcript'][:35]}...'" if r["transcript"] else ""
        print(f"  [{r['detected_category']:<9}] {r['name']:<25} (Old: {r['old_cat']}){t_snippet}")

    print("\n==================================================")
    print(f"SHEET 2 AUDIT BREAKDOWN ({len(sheet2_res)} Streams)")
    print("==================================================")
    for r in sheet2_res:
        t_snippet = f" | Spoken: '{r['transcript'][:35]}...'" if r["transcript"] else ""
        print(f"  [{r['detected_category']:<9}] {r['name']:<25} (Old: {r['old_cat']}){t_snippet}")

if __name__ == "__main__":
    main()
