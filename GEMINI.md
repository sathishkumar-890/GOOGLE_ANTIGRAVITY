# Master Workspace Instructions & Task Router

## Workspace Role & Task Overview
This repository contains 3 distinct maritime data processing tasks. Whenever the user initiates a conversation, identify which task they are working on and strictly follow the respective guidelines and directory scope.

---

### Task 1: Vessel Particulars & Machinery List (`VL_EXTRACTION`)
- **Working Directory**: `01_VL_EXTRACTION/`
- **Rule Document**: `01_VL_EXTRACTION/VL_RULES.md`
- **Key Files**: `VL_IRENE WISDOM.xlsx`, `B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf`, `update_pages_*.py`
- **Scope**: Extract machinery models, makers, serial numbers, component lists, and weights into `VL_IRENE WISDOM.xlsx`.

---

### Task 2: Technical Drawing & Photo Processing (`PHOTO_EDITING`)
- **Working Directory**: `02_PHOTO_EDITING/`
- **Rule Document**: `02_PHOTO_EDITING/PHOTO_RULES.md`
- **Subfolders**: `02_PHOTO_EDITING/raw_pages/`, `02_PHOTO_EDITING/cropped/`
- **Scope**: Page screenshot rendering, diagram cropping, table isolate crops, and OCR image enhancement.

---

### Task 3: Maritime Spare Parts PMS Extraction (`SPARE_EXTRACTION`)
- **Working Directory**: `03_SPARE_EXTRACTION/`
- **Rule Document**: `03_SPARE_EXTRACTION/PMS_RULES.md`
- **Key Files**: `TEMPLATE_PMS_SPARES.xlsx`, `verify_pms_spares.py`, ship technical PDFs, `SATHISH_*.xlsx`
- **Scope**: Strict PMS extraction into the 4-sheet template (100% UPPERCASE, character limits, intact V:AA formulas, 0 PMS validation errors).

---

## Shared Progress Tracking
Always refer to and update `PROGRESS.md` at the project root for the active task status and next steps when completing work.
