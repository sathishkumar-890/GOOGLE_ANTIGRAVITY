import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

targets = [
    'LOADING', 'LAODING', 'COMPUTER',
    'SHIPSIDE', 'VALVE',
    'EARTHING', 'SHAFT EARTHING',
    'AIR RESERVOIR', 'RESEVOIR',
    'COOLER', 'HEAT EXCHANGER', 'CENTRAL',
    'AMP', 'SHORE', 'ALTERNATIVE MARINE',
    'CCTV',
    'RADAR', 'RDR',
    'BATTERY', 'CHARGER',
    'ELEVATOR',
    'AIR CONDITION',
    'SCRUBBER', 'SOX',
    'SEWAGE',
    'STEERING'
]

results = {}
for t in targets:
    results[t] = []
    for it in items:
        m = it['machinery'].upper()
        f = it['function'].upper()
        h = it['hyperlink'].upper()
        p = it['parent'].upper()
        if t in m or t in f or t in h:
            results[t].append((it['machinery'], it['function'], it['hyperlink'], it['row']))

for t in targets:
    if results[t]:
        print(f"\n=== TARGET: {t} ({len(results[t])} matches) ===")
        seen = set()
        for m, f, h, r in results[t]:
            if (m, f) not in seen:
                seen.add((m, f))
                print(f"  Row {r}: Mach='{m}' -> Func='{f}' (Hyperlink: '{h[:40]}')")
