import openpyxl

wb_fun = openpyxl.load_workbook('01_VL_EXTRACTION/C.V. IRENES REWARD_FUN.xlsx', data_only=True)
ws_fun = wb_fun['Allocation Sheet']

fun_data = []
for r in range(12, ws_fun.max_row + 1):
    func = ws_fun.cell(r, 9).value
    mach = ws_fun.cell(r, 10).value
    hyper = ws_fun.cell(r, 3).value
    item_type = ws_fun.cell(r, 5).value
    if mach and mach != 'Folder' and func and func != 'Folder':
        fun_data.append({
            'row': r,
            'function': str(func).strip(),
            'machinery': str(mach).strip(),
            'hyperlink': str(hyper).strip() if hyper else '',
            'item_type': str(item_type).strip() if item_type else ''
        })

print(f'Total valid items extracted: {len(fun_data)}')

# Print first 30 unique machinery names and their functions
seen = set()
count = 0
for d in fun_data:
    key = (d['machinery'], d['function'])
    if key not in seen:
        seen.add(key)
        count += 1
        if count <= 40:
            print(f"{count:2d}. Mach: {d['machinery']}  -->  Func: {d['function']}")

print(f'\nTotal unique (machinery, function) pairs: {len(seen)}')
