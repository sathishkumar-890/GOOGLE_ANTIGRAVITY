import json
import sys
sys.path.append('01_VL_EXTRACTION')
from build_reward_function_mapping import get_function_for_reward_row, valid_funcs

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

unmapped = []
invalid = []
results = []

for r in main_rows:
    fn, mach = get_function_for_reward_row(
        r['row'], r['loc_code'], r['loc_desc'], r['sys_desc'], r['maker'], r['model'], r['particulars']
    )
    if not fn:
        unmapped.append(r)
    elif fn not in valid_funcs:
        invalid.append((r, fn))
    else:
        results.append((r['row'], r['loc_code'], r['loc_desc'], fn, mach))

print(f"Total rows: {len(main_rows)}")
print(f"Successfully mapped: {len(results)} / {len(main_rows)}")
print(f"Unmapped: {len(unmapped)}")
print(f"Invalid functions: {len(invalid)}")

# Verify our 3 key checks:
for row_num, lc, ld, fn, mach in results:
    if lc in ['AP', 'EGCS', 'SIGLTCOL']:
        print(f"Verified Row {row_num:3d} | [{lc:8s}] {ld:30s} -> FUNC: '{fn}' (MACH: '{mach}')")
