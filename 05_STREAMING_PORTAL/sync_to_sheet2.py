import requests
import csv
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

def sync_sheet2():
    with open("05_STREAMING_PORTAL/Sheet2_Deduplicated_Updated.csv", "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    print(f"Preparing to sync {len(rows)} rows to Sheet 2...")
    payload = {
        "action": "sync_all",
        "sheetName": "Sheet2",
        "rows": rows
    }
    
    r = requests.post(WEBHOOK_URL, json=payload, timeout=90)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    sync_sheet2()
