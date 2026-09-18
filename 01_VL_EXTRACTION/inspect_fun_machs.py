import json

with open('01_VL_EXTRACTION/reward_fun_items.json', 'r', encoding='utf-8') as f:
    fun_items = json.load(f)

with open('01_VL_EXTRACTION/reward_main_vdc_rows.json', 'r', encoding='utf-8') as f:
    main_rows = json.load(f)

print(f"Loaded {len(fun_items)} fun items, {len(main_rows)} main rows")

# Let's inspect the unique machineries in fun_items
fun_mach_map = {} # uppercase mach -> (func, original_mach)
for item in fun_items:
    m = item['machinery'].strip().upper()
    f = item['function'].strip()
    if m not in fun_mach_map:
        fun_mach_map[m] = []
    fun_mach_map[m].append(item)

print(f"Total unique uppercase machineries in FUN: {len(fun_mach_map)}")

# Let's see some samples of FUN machineries
for m in sorted(fun_mach_map.keys())[:30]:
    funcs = list(set(x['function'] for x in fun_mach_map[m]))
    print(f"  {m:45s} -> {funcs}")
