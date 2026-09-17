# Master Workspace Instructions & Task Router

## Workspace Role & Task Overview
This repository contains maritime data processing tasks, sister vessel comparisons, and chat archives. Whenever initiating a conversation, identify which task is active and strictly follow the respective guidelines and directory scope.

---

### Task 1: Vessel Particulars & Machinery List (`VL_EXTRACTION`)
- **Working Directory**: `01_VL_EXTRACTION/`
- **Rule Document**: `01_VL_EXTRACTION/VL_RULES.md`
- **Key Workbooks**:
  - `VL_IRENE WISDOM.xlsx` & `VL_IRENE WISDOM (1).xlsx` (Master with `LOCATION_CODE` & `SYSTEM_CODE`)
  - `VL_IRENES REWARD.xlsx` (Sister vessel comparison workbook with red highlights)
- **Source Booklets**:
  - `B-23_DATA BOOKLETS (MACHINERY PARTICULAR LIST).pdf`
  - `B-23_DATA BOOKLETS(MACHINERY PARTICULAR LIST IRENES REWARD) (1).pdf`
- **Scope**: Extract machinery models, makers, serial numbers, component lists, weights, and unique codes.

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

### Chat Archives & Cross-Machine Sync (`04_CHAT_ARCHIVES`)
- **Working Directory**: `04_CHAT_ARCHIVES/`
- **Export Script**: `python export_chats.py`
- **Scope**: Automated export of all Antigravity chat histories into human-readable Markdown files synced directly to GitHub so conversations are never lost across machines.

---

## Shared Progress Tracking
Always refer to and update `PROGRESS.md` at the project root for the active task status and next steps when completing work.
