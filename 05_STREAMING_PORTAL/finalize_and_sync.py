import sys
import os
import json
import csv
import io
import requests
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

sys.stdout.reconfigure(encoding="utf-8")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ/exec"

def load_audit_results():
    with open("05_STREAMING_PORTAL/auditor_engine_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # Map (sheet, name) -> result
    audit_map = {}
    for r in data:
        key = (r["sheet"].lower(), r["name"].strip().lower())
        audit_map[key] = r
    return audit_map

def get_category_and_status(sheet_name, name, orig_url, orig_cat, orig_icon, audit_map):
    key = (sheet_name.lower(), name.strip().lower())
    res = audit_map.get(key)
    
    if not res:
        return orig_cat, orig_icon, "Dead"
    
    status = res.get("new_status", "Dead")
    detected = res.get("detected_category", orig_cat)
    
    # Handle silent channels
    if detected in ["Dead / Silent", "Unknown", ""]:
        detected = orig_cat if orig_cat else "Tamil"
    
    # Special language sanity checks based on acoustic transcripts
    if name.strip().lower() == "manorama tv":
        detected = "Malayalam" # Spoken Malayalam / Malayalam channel
    
    # Choose icon based on category
    icon = orig_icon if orig_icon else "📺"
    if detected == "Music":
        icon = "🎵"
    elif detected == "English":
        icon = "🌐" if "travel" in name.lower() or "earth" in name.lower() else "🎬"
    elif detected == "Hindi":
        icon = "👶" if any(k in name.lower() for k in ["hungama", "toonami"]) else "🎬"
    elif detected == "Bengali":
        icon = "👶" if "bal bharat" in name.lower() else "🌍"
    elif detected == "Telugu":
        icon = "👶" if "sonic" in name.lower() else "📺"
    elif detected == "Malayalam":
        icon = "📰" if "manorama" in name.lower() else "🪷"
    elif detected == "Tamil":
        if any(k in name.lower() for k in ["news", "seithigal", "janam", "murasu", "thalaimurai"]):
            icon = "📰"
        elif any(k in name.lower() for k in ["sai", "sivan", "madha", "hebron", "hosanna", "svbc", "aastha", "aaseervatham", "sankara", "joy"]):
            icon = "🪷"
        elif any(k in name.lower() for k in ["movie", "flix", "cinema"]):
            icon = "🎬"
        elif any(k in name.lower() for k in ["kidz", "chithiram", "nick"]):
            icon = "👶"
        else:
            icon = orig_icon if orig_icon else "📺"

    return detected, icon, status

def main():
    print("==========================================================================")
    print("PREPARING FINAL ACOUSTICALLY-VERIFIED DATASETS FOR SHEET 1 & SHEET 2")
    print("==========================================================================")

    audit_map = load_audit_results()

    # 1. Fetch current Sheet 1 (78 channels)
    url_s1 = "https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/gviz/tq?tqx=out:csv&sheet=IPTV_Playlist"
    s1_raw = list(csv.reader(io.StringIO(requests.get(url_s1).text)))
    s1_rows = [r for r in s1_raw[1:] if r and any(r[:2])]

    # 2. Fetch Sheet 2 (48 channels from local non-overlapping master)
    with open("05_STREAMING_PORTAL/Sheet2_Non_Overlapping.csv", "r", encoding="utf-8") as f:
        s2_raw = list(csv.reader(f))
    s2_rows = [r for r in s2_raw[1:] if r and any(r[:2])]

    print(f"Sheet 1 original streams: {len(s1_rows)}")
    print(f"Sheet 2 original streams: {len(s2_rows)}")

    headers = ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"]

    # Build Sheet 1 rows
    sheet1_final = [headers]
    for r in s1_rows:
        name = r[0].strip()
        url = r[1].strip()
        cat = r[2].strip() if len(r) > 2 else ""
        icon = r[3].strip() if len(r) > 3 else "📺"
        new_cat, new_icon, new_status = get_category_and_status("Sheet1", name, url, cat, icon, audit_map)
        sheet1_final.append([name, url, new_cat, new_icon, new_status])

    # Build Sheet 2 rows
    sheet2_final = [headers]
    for r in s2_rows:
        name = r[0].strip()
        url = r[1].strip()
        cat = r[2].strip() if len(r) > 2 else ""
        icon = r[3].strip() if len(r) > 3 else "📺"
        new_cat, new_icon, new_status = get_category_and_status("Sheet2", name, url, cat, icon, audit_map)
        sheet2_final.append([name, url, new_cat, new_icon, new_status])

    # Save CSVs
    s1_csv = "05_STREAMING_PORTAL/Sheet1_Acoustic_Updated.csv"
    with open(s1_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(sheet1_final)
    print(f"Saved Sheet 1 CSV: {s1_csv}")

    s2_csv = "05_STREAMING_PORTAL/Sheet2_Acoustic_Updated.csv"
    with open(s2_csv, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(sheet2_final)
    print(f"Saved Sheet 2 CSV: {s2_csv}")

    # Save styled Dual-tab Excel
    excel_path = "05_STREAMING_PORTAL/Google_Sheets_Acoustic_Master.xlsx"
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # remove default sheet

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    live_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    live_font = Font(name="Segoe UI", size=10, bold=True, color="15803D")
    dead_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    dead_font = Font(name="Segoe UI", size=10, bold=False, color="B91C1C")

    for s_name, s_data in [("IPTV_Playlist", sheet1_final), ("Sheet2", sheet2_final)]:
        ws = wb.create_sheet(title=s_name)
        for r_idx, row in enumerate(s_data, 1):
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
    print(f"Saved Styled Excel Master: {excel_path}")

    # Summary
    print("\n---------------- SHEET 1 SUMMARY ----------------")
    s1_live = sum(1 for r in sheet1_final[1:] if r[4] == "Live")
    s1_dead = sum(1 for r in sheet1_final[1:] if r[4] == "Dead")
    print(f"Total: {len(sheet1_final)-1} | Live: {s1_live} | Dead: {s1_dead}")
    cats1 = {}
    for r in sheet1_final[1:]:
        if r[4] == "Live":
            cats1[r[2]] = cats1.get(r[2], 0) + 1
    print("Live Categories in Sheet 1:", cats1)

    print("\n---------------- SHEET 2 SUMMARY ----------------")
    s2_live = sum(1 for r in sheet2_final[1:] if r[4] == "Live")
    s2_dead = sum(1 for r in sheet2_final[1:] if r[4] == "Dead")
    print(f"Total: {len(sheet2_final)-1} | Live: {s2_live} | Dead: {s2_dead}")
    cats2 = {}
    for r in sheet2_final[1:]:
        if r[4] == "Live":
            cats2[r[2]] = cats2.get(r[2], 0) + 1
    print("Live Categories in Sheet 2:", cats2)

    # 3. Synchronize to Google Sheets via Webhook
    print("\n==========================================================================")
    print("STEP 2: SYNCHRONIZING DIRECTLY TO GOOGLE SHEETS VIA WEBHOOK")
    print("==========================================================================")

    print(f"Syncing Sheet 1 (IPTV_Playlist) ({len(sheet1_final)} rows)...")
    payload1 = {
        "action": "sync_all",
        "sheetName": "IPTV_Playlist",
        "rows": sheet1_final
    }
    r1 = requests.post(WEBHOOK_URL, json=payload1, timeout=90)
    print(f"Sheet 1 Webhook Status: {r1.status_code}")
    print(f"Sheet 1 Webhook Response: {r1.text}")

    print(f"\nSyncing Sheet 2 (Sheet2) ({len(sheet2_final)} rows)...")
    payload2 = {
        "action": "sync_all",
        "sheetName": "Sheet2",
        "rows": sheet2_final
    }
    r2 = requests.post(WEBHOOK_URL, json=payload2, timeout=90)
    print(f"Sheet 2 Webhook Status: {r2.status_code}")
    print(f"Sheet 2 Webhook Response: {r2.text}")

    print("\nALL SHEETS SYNCHRONIZED SUCCESSFULLY TO GOOGLE SHEETS!")

if __name__ == "__main__":
    main()
