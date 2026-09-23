import json
import csv
import io
import os
import sys
import requests
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

API_TOKEN = "1586305d6c74d4eb694d0ecfe4cf156e21714880"
USERNAME = "sathishkumar890"
BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"
HEADERS = {"Authorization": f"Token {API_TOKEN}"}
WEBAPP_DOMAIN = f"{USERNAME}.pythonanywhere.com"

def main():
    print("==========================================================================")
    print("FINALIZING WEB-APP-ONLY PLAYABLE STREAMS (TEXT ONLY, 0 HIGHLIGHTS)")
    print("==========================================================================")

    with open("05_STREAMING_PORTAL/webapp_stream_test_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    live_items = [d for d in data if d.get("web_ok")]
    dead_items = [d for d in data if not d.get("web_ok")]

    header = ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"]

    # Use 'LIVE' and 'DEAD' to avoid triggering Apps Script green/red background highlight rule
    s1_rows = [[d["name"], d["url"], d["cat"], d["icon"], "LIVE"] for d in live_items]
    s2_rows = [[d["name"], d["url"], d["cat"], d["icon"], "DEAD"] for d in dead_items]

    final_sheet1 = [header] + s1_rows
    final_sheet2 = [header] + s2_rows

    print(f"Sheet 1 (Web App Playable Only): {len(s1_rows)} streams")
    print(f"Sheet 2 (Dead / Non-Web Playable): {len(s2_rows)} streams")

    # 1. Save CSVs
    s1_csv = "05_STREAMING_PORTAL/Sheet1_Merged_Final.csv"
    with open(s1_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet1)
    print(f"Saved: {s1_csv}")

    s2_csv = "05_STREAMING_PORTAL/Sheet2_Dead_Only.csv"
    with open(s2_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet2)
    print(f"Saved: {s2_csv}")

    portal_csv = "05_STREAMING_PORTAL/IPTV_Playlist_Merged_Primary.csv"
    with open(portal_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet1)
    print(f"Saved Portal Playlist: {portal_csv}")

    # 2. Save Excel Master (Text Only, Zero Background Fills)
    excel_path = "05_STREAMING_PORTAL/Google_Sheets_Complete_Master.xlsx"
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    text_font = Font(name="Segoe UI", size=10, bold=False, color="000000")

    for title, rows_data in [("IPTV_Playlist", final_sheet1), ("Sheet2", final_sheet2)]:
        ws = wb.create_sheet(title=title)
        for r_idx, row in enumerate(rows_data, 1):
            for c_idx, val in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=val)
                if r_idx == 1:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    # Clean text only - NO fill color on any status!
                    cell.font = text_font
                    if c_idx == 5:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

        ws.column_dimensions["A"].width = 28
        ws.column_dimensions["B"].width = 65
        ws.column_dimensions["C"].width = 16
        ws.column_dimensions["D"].width = 10
        ws.column_dimensions["E"].width = 14

    wb.save(excel_path)
    print(f"Saved Excel master (clean text only, 0 highlights): {excel_path}")

    # 3. Deploy updated playlist file to PythonAnywhere
    print("\nDeploying clean 42-channel playlist to PythonAnywhere...")
    with open(portal_csv, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/files/path/home/{USERNAME}/Testproject/IPTV_Playlist_Merged_Primary.csv",
            headers=HEADERS,
            files={"content": f}
        )
        print(f"Uploaded playlist CSV to PythonAnywhere: {resp.status_code}")

    r_reload = requests.post(f"{BASE_URL}/webapps/{WEBAPP_DOMAIN}/reload/", headers=HEADERS)
    print(f"PythonAnywhere web app reloaded: {r_reload.status_code}")

    # 4. Synchronize both sheets to Google Sheets via Webhook
    print("\nSynchronizing Sheet 1 (IPTV_Playlist) to Google Sheets...")
    p1 = {"action": "sync_all", "sheetName": "IPTV_Playlist", "rows": final_sheet1}
    r1 = requests.post(WEBHOOK_URL, json=p1, timeout=60)
    print(f"Sheet 1 Sync Status: {r1.status_code}, Response: {r1.text}")

    print("Synchronizing Sheet 2 (Sheet2) to Google Sheets...")
    p2 = {"action": "sync_all", "sheetName": "Sheet2", "rows": final_sheet2}
    r2 = requests.post(WEBHOOK_URL, json=p2, timeout=60)
    print(f"Sheet 2 Sync Status: {r2.status_code}, Response: {r2.text}")

    print("\nALL TASKS SUCCESSFULLY COMPLETED!")

if __name__ == "__main__":
    main()
