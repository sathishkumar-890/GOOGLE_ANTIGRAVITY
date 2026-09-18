import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    fitems = json.load(f)

for it in fitems:
    if 'FIRE' in it['machinery'].upper():
        print(f"Row {it['row']:3d}: Mach='{it['machinery']}' -> Func='{it['function']}' (Hyperlink: '{it['hyperlink']}')")
