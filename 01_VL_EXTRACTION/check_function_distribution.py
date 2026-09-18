import json
from collections import Counter

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

import sys
sys.path.append('01_VL_EXTRACTION')
from test_full_reward_mapping import map_reward_row

counts = Counter()
for r in main_rows:
    fn, mach = map_reward_row(r)
    counts[fn] += 1

print("Distribution of Functions across 278 equipment rows:")
for fn, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {fn:42s}: {c:3d} rows")

print(f"\nTotal rows: {sum(counts.values())}")
print(f"Total distinct functions used: {len(counts)}")
