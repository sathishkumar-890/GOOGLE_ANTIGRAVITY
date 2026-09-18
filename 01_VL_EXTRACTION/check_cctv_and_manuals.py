import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    fun_items = json.load(f)

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

# Search for CCTV
cctv_matches = [it for it in fun_items if 'CCTV' in it['machinery'].upper() or 'CCTV' in it['hyperlink'].upper()]
print(f"CCTV matches in FUN ({len(cctv_matches)}):")
for it in cctv_matches:
    print(f"  Row {it['row']}: Mach='{it['machinery']}' -> Func='{it['function']}' (Hyperlink: '{it['hyperlink']}')")

# Check manual names in main_rows and see how many match hyperlinks in fun_items
# Notice manual_name in main_rows: 'B-23_DATA BOOKLETS(MACHINERY PARTICULAR LIST).pdf' is the booklet.
# But does main_rows or sheet Reward have individual manual names?
import openpyxl
wb = openpyxl.load_workbook('01_VL_EXTRACTION/VL_EXTRACTION_I.REWARD_MAIN VDC.xlsx', data_only=True)
ws_rew = wb['Reward']
print("\nSample Manual Names from sheet Reward (Col 10):")
manuals_sheet_rew = {}
for r in range(2, ws_rew.max_row + 1):
    m = ws_rew.cell(r, 10).value
    lc = ws_rew.cell(r, 1).value
    if m:
        manuals_sheet_rew[str(lc).strip().upper()] = str(m).strip()

print(f"Found {len(manuals_sheet_rew)} rows with manual names in sheet Reward")
for lc, m in list(manuals_sheet_rew.items())[:10]:
    print(f"  [{lc}]: {m}")
