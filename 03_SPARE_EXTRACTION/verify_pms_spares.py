import sys
import os
import re
import openpyxl

FORBIDDEN_CHARS_COMMON = ['%', '⌀', 'Φ', 'φ', '"', '″', '~', '?', '*', '●', '‣', '<=', '>=']

def verify_workbook(filepath):
    print(f"=== Verifying {filepath} ===")
    if not os.path.exists(filepath):
        print(f"[FAIL] Error: File not found {filepath}")
        return False

    wb = openpyxl.load_workbook(filepath, data_only=False)
    sheet_names = wb.sheetnames
    spares_sheet_name = None
    for name in ['Spares', 'SPARES']:
        if name in sheet_names:
            spares_sheet_name = name
            break
    if not spares_sheet_name:
        print(f"[FAIL] Missing required Spares sheet (neither 'Spares' nor 'SPARES' found). Sheets present: {sheet_names}")
        return False

    required_other_sheets = ['Rules', 'Sheet2', 'Sheet3']
    for s in required_other_sheets:
        if s not in sheet_names:
            print(f"[FAIL] Missing required sheet: {s}")
            return False
    print(f"[OK] All 4 sheets present (Spares sheet: '{spares_sheet_name}').")

    ws = wb[spares_sheet_name]
    errors = []
    data_rows = 0

    for r in range(2, 501):
        has_data = any(ws.cell(r, c).value is not None for c in range(1, 22))
        if has_data:
            data_rows += 1
            loc_code = str(ws.cell(r, 1).value or '')
            sub_code = str(ws.cell(r, 8).value or '')
            sub_desc = str(ws.cell(r, 9).value or '')
            item_code = str(ws.cell(r, 10).value or '')
            short_desc = str(ws.cell(r, 11).value or '')
            long_desc = str(ws.cell(r, 12).value or '')
            pos_no = str(ws.cell(r, 17).value or '')
            qty = str(ws.cell(r, 19).value or '')

            # Check lengths
            if len(sub_code) > 8:
                errors.append(f"Row {r}: Subsystem Code > 8 chars ({len(sub_code)}): '{sub_code}'")
            if len(sub_desc) > 60:
                errors.append(f"Row {r}: Subsystem Description > 60 chars ({len(sub_desc)}): '{sub_desc}'")
            if len(item_code) > 25:
                errors.append(f"Row {r}: Item Code > 25 chars ({len(item_code)}): '{item_code}'")
            if len(short_desc) > 60:
                errors.append(f"Row {r}: Short Description > 60 chars ({len(short_desc)}): '{short_desc}'")

            # Check uppercase
            for name, val in [("Subsystem Description", sub_desc), ("Item Code", item_code), ("Short Description", short_desc), ("Long Description", long_desc)]:
                if any(c.islower() for c in val):
                    errors.append(f"Row {r}: Lowercase characters found in {name}: '{val}'")

            # Check forbidden chars in all columns
            for name, val in [("Subsystem Description", sub_desc), ("Item Code", item_code), ("Short Description", short_desc), ("Long Description", long_desc)]:
                for fc in FORBIDDEN_CHARS_COMMON:
                    if fc in val:
                        errors.append(f"Row {r}: Forbidden character '{fc}' found in {name}: '{val}'")

            # Check parentheses forbidden in Item Code and Short Description
            for name, val in [("Item Code", item_code), ("Short Description", short_desc)]:
                if '(' in val or ')' in val:
                    errors.append(f"Row {r}: Forbidden parenthesis found in {name}: '{val}'")

            # Check comma spacing
            for name, val in [("Subsystem Description", sub_desc), ("Short Description", short_desc), ("Long Description", long_desc)]:
                if re.search(r',[^ ]', val):
                    errors.append(f"Row {r}: Comma without following space in {name}: '{val}'")

            # Check hyphens / slashes spacing (no spaces around hyphen or slash in codes/names)
            for name, val in [("Item Code", item_code), ("Short Description", short_desc)]:
                if ' -' in val or '- ' in val:
                    errors.append(f"Row {r}: Spaces around hyphen in {name}: '{val}'")
                if ' /' in val or '/ ' in val:
                    errors.append(f"Row {r}: Spaces around slash in {name}: '{val}'")

            # Check double spaces
            for name, val in [("Subsystem Description", sub_desc), ("Item Code", item_code), ("Short Description", short_desc)]:
                if '  ' in val:
                    errors.append(f"Row {r}: Double spaces in {name}: '{val}'")

        # Check formulas in V-AA down to 500
        f_v = str(ws.cell(r, 22).value or '')
        f_w = str(ws.cell(r, 23).value or '')
        f_x = str(ws.cell(r, 24).value or '')
        f_y = str(ws.cell(r, 25).value or '')
        f_z = str(ws.cell(r, 26).value or '')
        f_aa = str(ws.cell(r, 27).value or '')

        if not f_v.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col V: '{f_v}'")
        if not f_w.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col W: '{f_w}'")
        if not f_x.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col X: '{f_x}'")
        if not f_y.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col Y: '{f_y}'")
        if not f_z.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col Z: '{f_z}'")
        if not f_aa.startswith('='):
            errors.append(f"Row {r}: Missing formula in Col AA: '{f_aa}'")

    print(f"Total populated data rows: {data_rows}")
    if errors:
        print(f"[FAIL] Found {len(errors)} errors:")
        for e in errors[:20]:
            print("  -", e)
        if len(errors) > 20:
            print(f"  ... and {len(errors)-20} more errors.")
        return False
    else:
        print("[OK] ALL PMS VALIDATION RULES PASSED WITH 0 ERRORS!")
        return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TEMPLATE_PMS_SPARES.xlsx")
    success = verify_workbook(target)
    sys.exit(0 if success else 1)
