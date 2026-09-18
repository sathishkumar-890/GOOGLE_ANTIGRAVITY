import json

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

import sys
sys.path.append('01_VL_EXTRACTION')
from test_full_reward_mapping import map_reward_row

print("Checking specific equipment rows:")
specific_checks = [
    'STEERING GEAR ROOM SUPPLY FAN',
    'BOW THRUSTER ROOM SUPPLY FAN',
    'TREATED SEWAGE DISCHARGE PUMP',
    'SEWAGE TREATMENT PLANT',
    'CREW ELEVATOR',
    'LOADING COMPUTER',
    'AMP SYSTEM',
    'AIR CONDITIONING',
    'A/C PLANT',
    'AIR HANDLING UNIT',
    'CENTRAL F.W COOLER',
    'F.O.SUPPLY UNIT',
    'M/E AUTO L.O. FILTER',
    'MARINE RADAR',
    'CCTV',
    'HOSPITAL CALLING',
    'REF. CHAMBER'
]

for r in main_rows:
    ld = str(r['loc_desc'] or '').upper()
    for sc in specific_checks:
        if sc in ld:
            fn, mach = map_reward_row(r)
            print(f"Row {r['row']:3d} | [{r['loc_code']:8s}] {r['loc_desc']:38s} -> Func: '{fn}' (Mach: '{mach}')")
