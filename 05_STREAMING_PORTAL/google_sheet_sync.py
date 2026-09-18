"""
Google Sheets Webhook Sync Utility
Enables direct, real-time read and write control over the user's Google Sheet via Google Apps Script Web App.
"""

import sys
import json
import requests

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

def ping():
    """Health check on the Web App endpoint."""
    try:
        r = requests.get(WEBHOOK_URL, timeout=15)
        print(f"[PING] Status Code: {r.status_code}")
        print(f"[PING] Response: {r.text}")
        return r.json()
    except Exception as e:
        print(f"[ERROR] Ping failed: {e}")
        return None

def update_statuses(url_to_status_dict):
    """
    Updates the STATUS column (Col 5) for matching URLs in the Google Sheet.
    url_to_status_dict: { "https://...": "Live", "https://...": "Dead" }
    """
    payload = {
        "action": "update_status",
        "updates": url_to_status_dict
    }
    try:
        print(f"[SYNC] Sending status updates for {len(url_to_status_dict)} channels...")
        r = requests.post(WEBHOOK_URL, json=payload, timeout=60)
        print(f"[SYNC] Status Code: {r.status_code}")
        print(f"[SYNC] Response: {r.text}")
        return r.json()
    except Exception as e:
        print(f"[ERROR] Update failed: {e}")
        return None

def sync_all(rows):
    """
    Overwrites the sheet with full 2D array of rows and formats colors.
    rows: [ ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"], ... ]
    """
    payload = {
        "action": "sync_all",
        "rows": rows
    }
    try:
        print(f"[SYNC_ALL] Overwriting sheet with {len(rows)} total rows...")
        r = requests.post(WEBHOOK_URL, json=payload, timeout=90)
        print(f"[SYNC_ALL] Status Code: {r.status_code}")
        print(f"[SYNC_ALL] Response: {r.text}")
        return r.json()
    except Exception as e:
        print(f"[ERROR] Sync all failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Google Sheets Webhook Sync")
    parser.add_argument("--ping", action="store_true", help="Test connectivity")
    args = parser.parse_args()

    if args.ping:
        ping()
    else:
        ping()
