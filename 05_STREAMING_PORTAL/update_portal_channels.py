import json
import csv
import os
import requests
import re

# 1. Load verification results
with open("05_STREAMING_PORTAL/verification_results_full.json", "r", encoding="utf-8") as f:
    verif_results = json.load(f)

# Map URL and row to verification result
url_result_map = {r["url"]: r for r in verif_results}
row_result_map = {r["row"]: r for r in verif_results}

# 2. Read updated Google Sheet CSV
with open("05_STREAMING_PORTAL/Google_Sheet_Updated_Status.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    sheet_rows = list(reader)

# Build unified channel list for modern_player.js
channel_items = []
seen_urls = set()

# Distinct icons mapping for categories
CAT_ICONS = {
    "Tamil": "📺",
    "English": "🌐",
    "Hindi": "🎬",
    "Malayalam": "📺",
    "Telugu": "📺",
    "Kids": "👶",
    "Music": "🎵",
    "News": "📰"
}

for idx, r in enumerate(sheet_rows):
    if not r or len(r) < 2:
        continue
    name = r[0].strip()
    url = r[1].strip()
    if name.upper() == "STREAM NAME" or not url.startswith("http"):
        continue

    # De-duplicate identical URL
    if url in seen_urls:
        continue
    seen_urls.add(url)

    cat = r[2].strip() if len(r) > 2 and r[2].strip() else "Tamil"
    icon = r[3].strip() if len(r) > 3 and r[3].strip() else CAT_ICONS.get(cat, "📺")
    status = r[4].strip() if len(r) > 4 else "Not Playing"

    verif = url_result_map.get(url) or row_result_map.get(idx + 1)
    is_playing = (status == "Playing") or (verif and verif.get("playing", False))
    resolution = verif.get("resolution", "") if verif else ""

    slug = re.sub(r'[^a-z0-9_]+', '_', name.lower()).strip('_')
    if not slug:
        slug = f"ch_{idx}"

    channel_items.append({
        "id": slug,
        "name": name,
        "cat": cat,
        "icon": icon,
        "url": url,
        "status": "Playing" if is_playing else "Offline",
        "live": bool(is_playing),
        "resolution": resolution
    })

# Prioritize playing channels first in the list
channel_items.sort(key=lambda x: (not x["live"], x["name"]))

print(f"Total unified unique channels: {len(channel_items)}")
playing_unified = sum(1 for c in channel_items if c["live"])
print(f"Verified Playing channels: {playing_unified}")
print(f"Offline channels: {len(channel_items) - playing_unified}")

# Save all_channels_merged.json
with open("05_STREAMING_PORTAL/all_channels_merged.json", "w", encoding="utf-8") as f:
    json.dump(channel_items, f, indent=2, ensure_ascii=False)
print("Updated 05_STREAMING_PORTAL/all_channels_merged.json")

# Update modern_player.js
js_path = "05_STREAMING_PORTAL/static/js/modern_player.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace const channelData = [...];
new_data_str = json.dumps(channel_items, indent=2, ensure_ascii=False)
pattern = r"const channelData = \[[\s\S]*?\];"
replacement = f"const channelData = {new_data_str};"

if re.search(pattern, js_content):
    js_content = re.sub(pattern, replacement, js_content)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated 05_STREAMING_PORTAL/static/js/modern_player.js")
else:
    print("Warning: const channelData pattern not matched in modern_player.js")

# Also update IPTV_Playlist_Updated.csv and .xlsx
updated_playlist_csv = "05_STREAMING_PORTAL/IPTV_Playlist_Updated.csv"
with open(updated_playlist_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS", "RESOLUTION"])
    for c in channel_items:
        writer.writerow([c["name"], c["url"], c["cat"], c["icon"], c["status"], c.get("resolution", "")])
print(f"Updated {updated_playlist_csv}")

# 3. Deploy to PythonAnywhere via REST API
API_TOKEN = "1586305d6c74d4eb694d0ecfe4cf156e21714880"
USERNAME = "sathishkumar890"
headers = {"Authorization": f"Token {API_TOKEN}"}
base_url = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

print("\n--- DEPLOYING TO PYTHONANYWHERE ---")

# Upload modern_player.js
remote_js_path = f"/home/{USERNAME}/Testproject/static/js/modern_player.js"
print(f"Uploading modern_player.js to {remote_js_path}...")
with open(js_path, "rb") as f:
    r_js = requests.post(
        f"{base_url}/files/path{remote_js_path}",
        headers=headers,
        files={"content": f}
    )
print(f"Upload modern_player.js Status: {r_js.status_code}")

# Reload Web App
webapp_domain = f"{USERNAME}.pythonanywhere.com"
print(f"Reloading {webapp_domain}...")
r_reload = requests.post(
    f"{base_url}/webapps/{webapp_domain}/reload/",
    headers=headers
)
print(f"Reload Status: {r_reload.status_code}")

if r_reload.status_code == 200:
    print("Successfully reloaded web application on PythonAnywhere!")
else:
    print(f"Reload Response: {r_reload.text}")
