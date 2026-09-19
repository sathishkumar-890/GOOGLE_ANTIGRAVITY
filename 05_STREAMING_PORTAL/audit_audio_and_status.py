import urllib.request
import urllib.parse
import csv
import io
import re
import ssl
import sys

sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/export?format=csv"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode("utf-8")
reader = csv.reader(io.StringIO(data))
rows = list(reader)[1:]

print(f"Auditing {len(rows)} streams from Google Sheet...\n")

multi_audio = []
dead_streams = []
live_streams = []

for idx, r in enumerate(rows):
    name, stream_url = r[0].strip(), r[1].strip()
    try:
        req_stream = urllib.request.Request(stream_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req_stream, context=ctx, timeout=7) as stream_resp:
            content = stream_resp.read().decode("utf-8", errors="replace")
            live_streams.append((name, stream_url))
            
            # Check for audio tracks
            # e.g.: #EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="Tamil",DEFAULT=YES,AUTOSELECT=YES,LANGUAGE="tam",URI="..."
            lines = content.splitlines()
            audio_lines = [l for l in lines if l.startswith("#EXT-X-MEDIA:TYPE=AUDIO")]
            
            if len(audio_lines) > 1:
                track_info = []
                for al in audio_lines:
                    name_m = re.search(r'NAME="([^"]+)"', al)
                    lang_m = re.search(r'LANGUAGE="([^"]+)"', al)
                    t_name = name_m.group(1) if name_m else "Audio"
                    t_lang = lang_m.group(1) if lang_m else ""
                    track_info.append(f"{t_name} ({t_lang})" if t_lang else t_name)
                multi_audio.append((name, len(audio_lines), track_info, stream_url))
    except Exception as e:
        dead_streams.append((name, str(e), stream_url))

print(f"\n--- AUDIT SUMMARY ---")
print(f"Live / Reachable Streams: {len(live_streams)} / {len(rows)}")
print(f"Unreachable / Dead Streams: {len(dead_streams)} / {len(rows)}")

if dead_streams:
    print("\n[DEAD STREAMS]:")
    for d in dead_streams:
        print(f"  ❌ {d[0]}: {d[1][:80]}")

print(f"\n[MULTI-AUDIO STREAMS ({len(multi_audio)} FOUND)]:")
for m in multi_audio:
    print(f"  🎧 {m[0]} ({m[1]} Audio Tracks): {', '.join(m[2])}")
    print(f"     URL: {m[3]}")

# Save detailed results to JSON for plan & execution
results = {
    "total": len(rows),
    "live_count": len(live_streams),
    "dead_count": len(dead_streams),
    "dead_streams": [{"name": d[0], "error": d[1], "url": d[2]} for d in dead_streams],
    "multi_audio": [{"name": m[0], "count": m[1], "tracks": m[2], "url": m[3]} for m in multi_audio]
}

import json
with open("stream_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nSaved stream_audit_results.json")
