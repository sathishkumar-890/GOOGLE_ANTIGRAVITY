# Task 2: Technical Drawing & Photo Processing (PHOTO_EDITING)

## 1. Overview
Process ship technical drawings, manual page screenshots, machinery layout crops, and photo enhancements for verification and OCR inspection.

## 2. Directory Structure
- `02_PHOTO_EDITING/raw_pages/`: Full-page screenshots / rendered pages (e.g. `page_15.png`, `page_57.png`).
- `02_PHOTO_EDITING/cropped/`: Focused crops of specific tables, machinery plates, weight callouts, and section drawings (e.g. `crop_p57_weight.png`, `engine_crop.png`).

## 3. Standards & Best Practices
1. **Naming Conventions**:
   - Full pages: `page_<page_number>.png`
   - Focused crops: `crop_p<page_number>_<feature_name>.png` (e.g., `crop_p30_spec_table.png`)
2. **Quality & Clarity**:
   - Maintain original resolution or 300 DPI when rendering from PDF.
   - Crop tightly to the table or diagram of interest to minimize visual noise during OCR or inspection.
