# Task 1: Vessel Particulars & Machinery List Extraction (VL_EXTRACTION)

## 1. Overview
Extract machinery specifications, maker details, models, serial numbers, quantities, and weights from ship data booklets into the vessel particulars master workbook.

## 2. Key Files
- **Master Workbook**: `VL_IRENE WISDOM.xlsx` (Sheet: `VL_IRENE_WISDOM`)
- **Source Booklet**: `B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf`
- **Automation Scripts**: `update_pages_*.py` for automated row matching and cell population via `openpyxl`.

## 3. Extraction Standards
1. **Machinery Matching**: Match machinery item names from the PDF to existing rows in `VL_IRENE WISDOM.xlsx`.
2. **Maker & Model**:
   - Extract exact manufacturer/maker name (e.g., `HME`, `AUTRONICA`, `MRC`).
   - Extract exact model code. If not specified, set to `NA`.
3. **Serial Number**: If not listed, set to `NA`.
4. **Specification Format**:
   - Include all components, sub-units, quantities, and ratings:
     ```text
     MAIN CABINET : 1 EA
     - REPEATER PANEL : 1 EA
     - SMOKE DETECTOR : 33 EA
     WEIGHT : 34 KG
     ```
5. **Reference Traceability**: Record `B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf` and the exact source page number.
