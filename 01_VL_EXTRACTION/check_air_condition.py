import json

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

import sys
sys.path.append('01_VL_EXTRACTION')
from test_full_reward_mapping import map_reward_row

for r in main_rows:
    fn, mach = map_reward_row(r)
    if fn == 'AIR CONDITION':
        print(f"Row {r['row']:3d} | [{r['loc_code']:8s}] {r['loc_desc']:38s} | Sys: {r['sys_desc']}")
