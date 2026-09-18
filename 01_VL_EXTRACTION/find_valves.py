import json

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

for r in main_rows:
    ld = str(r['loc_desc'] or '').upper()
    sd = str(r['sys_desc'] or '').upper()
    lc = str(r['loc_code'] or '').upper()
    if 'VALVE' in ld or 'VALVE' in sd or 'VALVE' in lc:
        print(f"Row {r['row']:3d} | [{r['loc_code']:8s}] {r['loc_desc']:38s} | Sys: {r['sys_desc']}")
