import requests
import csv
import io

for name in ['IPTV', 'IPTV_Playlist', 'Sheet1', 'Sheet 1', 'Sheet2']:
    url = f'https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet={name}'
    r = requests.get(url)
    if r.status_code == 200:
        rows = list(csv.reader(io.StringIO(r.text)))
        print(f"Sheet '{name}': status={r.status_code}, rows={len(rows)}")
    else:
        print(f"Sheet '{name}': status={r.status_code}")
