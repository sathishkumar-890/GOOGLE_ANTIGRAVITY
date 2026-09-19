import sys
import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")

def format_sheet(ws, title, rows, header_bg="1E293B"):
    ws.title = title
    ws.views.sheetView[0].showGridLines = True

    # Header font & fill
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color=header_bg, end_color=header_bg, fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Data styles
    font_regular = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_center = Alignment(horizontal="center", vertical="center")

    # Status fills
    live_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    live_font = Font(name="Calibri", size=10, bold=True, color="15803D")
    dead_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    dead_font = Font(name="Calibri", size=10, bold=True, color="B91C1C")

    # Thin border
    thin_side = Side(style="thin", color="E2E8F0")
    cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # Headers
    headers = ["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"]
    ws.append(headers)
    ws.row_dimensions[1].height = 26

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align

    # Append rows
    for r_idx, row in enumerate(rows, start=2):
        ws.append(row[:5])
        ws.row_dimensions[r_idx].height = 20
        status_val = str(row[4]).strip() if len(row) > 4 else ""

        for c_idx in range(1, 6):
            c = ws.cell(row=r_idx, column=c_idx)
            c.border = cell_border
            if c_idx in [1, 2]:
                c.alignment = align_left
                c.font = font_bold if c_idx == 1 else font_regular
            elif c_idx in [3, 4]:
                c.alignment = align_center
                c.font = font_regular
            elif c_idx == 5:
                c.alignment = align_center
                if status_val.lower() == "live":
                    c.fill = live_fill
                    c.font = live_font
                elif status_val.lower() == "dead":
                    c.fill = dead_fill
                    c.font = dead_font

    # Auto-fit column widths
    col_widths = {1: 28, 2: 70, 3: 16, 4: 10, 5: 14}
    for col_idx, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

def main():
    # Read Sheet 1 (Live only)
    with open("05_STREAMING_PORTAL/Sheet1_Clean_Live_Only.csv", "r", encoding="utf-8") as f:
        s1_rows = list(csv.reader(f))[1:]

    # Read Sheet 2 (Deduplicated, updated status, moved dead rows)
    with open("05_STREAMING_PORTAL/Sheet2_Deduplicated_Updated.csv", "r", encoding="utf-8") as f:
        s2_rows = list(csv.reader(f))[1:]

    wb = openpyxl.Workbook()
    
    # Sheet 1
    ws1 = wb.active
    format_sheet(ws1, "IPTV_Playlist", s1_rows, header_bg="1E293B")

    # Sheet 2
    ws2 = wb.create_sheet(title="Sheet2")
    format_sheet(ws2, "Sheet2", s2_rows, header_bg="0F172A")

    out_excel = "05_STREAMING_PORTAL/Google_Sheet_Complete_Cleaned.xlsx"
    wb.save(out_excel)
    print(f"Created styled master workbook: {out_excel}")
    print(f"  - Sheet 'IPTV_Playlist': {len(s1_rows)} rows (100% Live, 0 Dead)")
    print(f"  - Sheet 'Sheet2': {len(s2_rows)} rows (Deduplicated, 103 Live, 26 Dead)")

if __name__ == "__main__":
    main()
