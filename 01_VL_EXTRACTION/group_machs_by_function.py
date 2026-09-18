import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

by_func = {}
for it in items:
    f = it['function']
    m = it['machinery']
    if f not in by_func:
        by_func[f] = set()
    by_func[f].add(m)

for f in sorted(by_func.keys()):
    machs = sorted(list(by_func[f]))
    print(f"\nFunction: {f} ({len(machs)} machineries):")
    for m in machs[:15]:
        print(f"  - {m}")
    if len(machs) > 15:
        print(f"  ... and {len(machs) - 15} more")
