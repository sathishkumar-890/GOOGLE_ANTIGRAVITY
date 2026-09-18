import json

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    rows = json.load(f)

for r in rows:
    ld = r['loc_desc'].upper()
    if any(k in ld for k in ['SAFE', 'EEBD', 'LSA', 'FFA', 'BREATH', 'JACKET', 'BUOY', 'SUIT']):
        print(f"Row {r['row']}: [{r['loc_code']}] {r['loc_desc']}")
