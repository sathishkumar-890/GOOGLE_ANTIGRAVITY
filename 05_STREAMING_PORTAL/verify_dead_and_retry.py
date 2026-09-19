import sys
import os
import re
import json
import subprocess
import numpy as np
import scipy.io.wavfile as wavfile
import speech_recognition as sr

sys.stdout.reconfigure(encoding="utf-8")

AUDIO_DIR = os.path.abspath("05_STREAMING_PORTAL/audio_samples")

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

def capture_stream(url, out_wav):
    cmd = [
        "ffmpeg", "-y",
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-rw_timeout", "10000000",
        "-analyzeduration", "3000000",
        "-probesize", "1500000",
        "-i", url,
        "-t", "5",
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        out_wav
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=14)
        if res.returncode == 0 and os.path.exists(out_wav) and os.path.getsize(out_wav) > 10000:
            return True, "Captured"
        err = res.stderr.decode("utf-8", errors="ignore")[-200:]
        if "404 Not Found" in err:
            return False, "404 Not Found"
        if "403 Forbidden" in err:
            return False, "403 Forbidden"
        return False, "Capture failed"
    except subprocess.TimeoutExpired:
        return False, "Timed out after 14s"
    except Exception as e:
        return False, str(e)[:50]

def analyze(wav_path, hint=""):
    try:
        sr_rate, data = wavfile.read(wav_path)
        if len(data) == 0:
            return "Dead / Silent", "", 0, "Empty"
        rms = float(np.sqrt(np.mean(data.astype(np.float32)**2)))
        if rms < 35:
            return "Dead / Silent", "", rms, "Inaudible"

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as src:
            audio = recognizer.record(src)

        prioritized = []
        hint_clean = hint.strip().title()
        for n, c in LANG_CONFIG:
            if n == hint_clean:
                prioritized.insert(0, (n, c))
            else:
                prioritized.append((n, c))

        texts = {}
        for n, c in prioritized:
            try:
                t = recognizer.recognize_google(audio, language=c)
                if t and len(t.strip()) > 0:
                    texts[n] = t.strip()
                    if n in SCRIPT_RANGES and count_script_chars(t, n) >= 3:
                        break
                    if n == "English" and len(t.split()) >= 3 and hint_clean == "English":
                        break
            except:
                pass

        if texts:
            best_lang = max(texts.keys(), key=lambda k: len(texts[k]))
            return best_lang, texts[best_lang], rms, f"Spoken speech identified ({best_lang})"

        zcr = float(np.mean(np.abs(np.diff(np.sign(data.astype(np.float32)))))) / 2.0
        return "Music", "", rms, f"Continuous music (RMS={rms:.1f}, ZCR={zcr:.4f})"
    except Exception as e:
        return "Unknown", "", 0, str(e)[:50]

def main():
    with open("05_STREAMING_PORTAL/auditor_engine_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    dead_items = [r for r in results if r["new_status"] != "Live"]
    print(f"Retrying {len(dead_items)} dead/timed-out streams with clean native user-agent...")

    updated_count = 0
    for item in dead_items:
        url = item["url"]
        name = item["name"]
        sheet = item["sheet"]
        idx = item["index"]
        hint = item["old_cat"]

        # Skip known defunct URLs that are truly dead
        if "dailyhunt" in url or "light-ott" in url or "404" in item["notes"] or "403" in item["notes"]:
            print(f"  [-] Skipping permanent dead: [{sheet}] #{idx:02d} {name} ({item['notes']})")
            continue

        slug = re.sub(r'[^a-zA-Z0-9_]+', '_', name.lower()).strip('_')
        out_wav = os.path.join(AUDIO_DIR, f"retry_{sheet}_{idx:02d}_{slug}.wav")

        ok, msg = capture_stream(url, out_wav)
        if ok:
            lang, txt, rms, note = analyze(out_wav, hint=hint)
            item["new_status"] = "Live"
            item["detected_category"] = lang
            item["transcript"] = txt
            item["rms"] = rms
            item["notes"] = note
            item["wav"] = out_wav
            updated_count += 1
            snip = f" | Spoken: '{txt[:30]}...'" if txt else f" ({note})"
            print(f"  [+] REVIVED: [{sheet}] #{idx:02d} {name:<22} -> [{lang}] {snip}")
        else:
            print(f"  [-] Confirmed Dead: [{sheet}] #{idx:02d} {name:<22} ({msg})")

    print(f"\nRevived {updated_count} streams! Saving updated results...")
    with open("05_STREAMING_PORTAL/auditor_engine_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
