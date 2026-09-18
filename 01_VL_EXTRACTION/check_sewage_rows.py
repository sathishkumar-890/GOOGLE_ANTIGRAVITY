import json

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

import sys
sys.path.append('01_VL_EXTRACTION')
from test_full_reward_mapping import map_reward_row

for r in main_rows:
    ld = str(r['loc_desc'] or '').upper()
    if 'SEWAGE' in ld:
        fn, mach = map_reward_row(r)
        print(f"Row {r['row']:3d} | [{r['loc_code']:8s}] {r['loc_desc']:38s} -> Func: '{fn}' (Mach: '{mach}')")
