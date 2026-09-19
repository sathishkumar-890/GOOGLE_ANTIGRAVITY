import requests
import csv
import io
import re
import sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

def norm_key(name):
    c = re.sub(r'\b(tv|hd)\b', '', name, flags=re.IGNORECASE)
    return re.sub(r'[^a-zA-Z0-9]+', '', c.lower())

def main():
    print("==========================================================================")
    print("MOVING LIVE CHANNELS FROM SHEET 2 TO SHEET 1 WITH TV1/TV2 COLLISION RESOLUTION")
    print("==========================================================================")

    # 1. Fetch current Sheet 1
    r1 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist")
    s1_raw = list(csv.reader(io.StringIO(r1.text)))
    s1_header = s1_raw[0][:5]
    s1_rows = [r[:5] for r in s1_raw[1:] if r and any(r[:2])]

    # 2. Fetch current Sheet 2
    r2 = requests.get("https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=Sheet2")
    s2_raw = list(csv.reader(io.StringIO(r2.text)))
    s2_header = s2_raw[0][:5]
    s2_rows = [r[:5] for r in s2_raw[1:] if r and any(r[:2])]

    s2_live = [r for r in s2_rows if len(r) > 4 and r[4].strip() == "Live"]
    s2_dead = [r for r in s2_rows if len(r) > 4 and r[4].strip() == "Dead"]

    print(f"Initial Sheet 1: {len(s1_rows)} rows")
    print(f"Initial Sheet 2: {len(s2_rows)} rows ({len(s2_live)} Live, {len(s2_dead)} Dead)")

    # Build mapping of norm_key to s1 rows
    s1_dict = {}
    for idx, r in enumerate(s1_rows):
        k = norm_key(r[0])
        s1_dict[k] = idx

    new_s1_rows = [list(r) for r in s1_rows]
    moved_rows = []

    for r in s2_live:
        new_r = list(r)
        k = norm_key(new_r[0])
        if k in s1_dict:
            s1_idx = s1_dict[k]
            orig_s1_name = new_s1_rows[s1_idx][0]
            base_name = re.sub(r'\s*\b(tv\d*|hd)\b\s*', ' ', orig_s1_name, flags=re.IGNORECASE).strip()
            if not base_name:
                base_name = orig_s1_name
            
            # Mention TV1 and TV2
            new_s1_rows[s1_idx][0] = f"{base_name} TV1"
            new_r[0] = f"{base_name} TV2"
            print(f"  [COLLISION RESOLVED]: '{orig_s1_name}' -> '{new_s1_rows[s1_idx][0]}' AND '{r[0]}' -> '{new_r[0]}'")
        moved_rows.append(new_r)

    final_sheet1 = [s1_header] + new_s1_rows + moved_rows
    final_sheet2 = [s2_header] + s2_dead

    print(f"\nFinal Sheet 1: {len(final_sheet1)-1} streams")
    print(f"Final Sheet 2: {len(final_sheet2)-1} streams (all Dead)")

    # Save to local CSVs
    s1_csv = "05_STREAMING_PORTAL/Sheet1_Merged_Final.csv"
    with open(s1_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet1)
    print(f"Saved: {s1_csv}")

    s2_csv = "05_STREAMING_PORTAL/Sheet2_Dead_Only.csv"
    with open(s2_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet2)
    print(f"Saved: {s2_csv}")

    # Also update portal primary playlist
    portal_csv = "05_STREAMING_PORTAL/IPTV_Playlist_Merged_Primary.csv"
    with open(portal_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(final_sheet1)
    print(f"Updated portal playlist: {portal_csv}")

    # Save styled Excel workbook
    excel_path = "05_STREAMING_PORTAL/Google_Sheets_Complete_Master.xlsx"
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    live_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    live_font = Font(name="Segoe UI", size=10, bold=True, color="15803D")
    dead_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    dead_font = Font(name="Segoe UI", size=10, bold=False, color="B91C1C")

    for title, data in [("IPTV_Playlist", final_sheet1), ("Sheet2", final_sheet2)]:
        ws = wb.create_sheet(title=title)
        for r_idx, row in enumerate(data, 1):
            for c_idx, val in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=val)
                if r_idx == 1:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    if c_idx == 5:
                        if val == "Live":
                            cell.fill = live_fill
                            cell.font = live_font
                        else:
                            cell.fill = dead_fill
                            cell.font = dead_font
                        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions["A"].width = 28
        ws.column_dimensions["B"].width = 65
        ws.column_dimensions["C"].width = 16
        ws.column_dimensions["D"].width = 10
        ws.column_dimensions["E"].width = 14

    wb.save(excel_path)
    print(f"Saved styled workbook: {excel_path}")

    # 3. Synchronize to Google Sheets via Webhook
    print("\n==========================================================================")
    print("STEP 2: SYNCHRONIZING TO GOOGLE SHEETS VIA APPS SCRIPT WEBHOOK")
    print("==========================================================================")

    print(f"Syncing Sheet 1 (IPTV_Playlist) ({len(final_sheet1)} rows)...")
    p1 = {
        "action": "sync_all",
        "sheetName": "IPTV_Playlist",
        "rows": final_sheet1
    }
    r1 = requests.post(WEBHOOK_URL, json=p1, timeout=90)
    print(f"Sheet 1 Status: {r1.status_code}, Response: {r1.text}")

    print(f"\nSyncing Sheet 2 (Sheet2) ({len(final_sheet2)} rows)...")
    p2 = {
        "action": "sync_all",
        "sheetName": "Sheet2",
        "rows": final_sheet2
    }
    r2 = requests.post(WEBHOOK_URL, json=p2, timeout=90)
    print(f"Sheet 2 Status: {r2.status_code}, Response: {r2.text}")

    print("\nSUCCESS: All changes synchronized to Google Sheets!")

if __name__ == "__main__":
    main()
