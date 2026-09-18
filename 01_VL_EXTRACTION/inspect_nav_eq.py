import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print("Navigation Equipment machineries:")
for it in items:
    if it['function'] == 'NAVIGATION EQUIPMENT':
        print(f"  - Mach: '{it['machinery']}' | Hyperlink: '{it['hyperlink']}'")
