# How to Export and Use this Data Extraction Task on Another Computer

This package contains everything needed to run maritime spare parts data extraction from ship manuals/drawings into PMS-compliant Excel workbooks on another computer.

---

## What Is Included in This Package

1. **`GEMINI.md`**:
   The complete system prompt and PMS rules file. When Antigravity opens this workspace, it automatically loads these rules.
2. **`TEMPLATE_PMS_SPARES.xlsx`**:
   The pristine Excel template containing all 4 required sheets (`SPARES`, `Rules`, `Sheet2`, `Sheet3`) and pre-configured validation formulas in columns `V` through `AA` down to row 500.
3. **`verify_pms_spares.py`**:
   Automated validator script that checks any extracted workbook against all strict PMS rules (lengths, uppercase, forbidden characters, comma/hyphen spacing, formulas).
4. **`requirements.txt`**:
   Python dependencies (`openpyxl`, `pypdf`, `pillow`).
5. **Sample Extracted Files**:
   - `SATHISH_FLOAT FREE EPIRB.pdf.xlsx`
   - `SATHISH_COMMON BATTERY TELEPHONE.pdf.xlsx`
   - `SATHISH_BATTERY CHARGING BOARD FOR GENERAL USE.pdf.xlsx`

---

## Method 1: Using Antigravity on Another Computer (Recommended)

If the other computer has Google Antigravity installed:

1. **Copy the Folder**:
   Copy the `Google_antigravity_project` folder (or extract `pms_spares_task_export.zip`) to your desired location on Computer B.
2. **Open the Project in Antigravity**:
   In Antigravity, click **Open Project** / **Open Folder** and select `Google_antigravity_project`.
3. **Automatic Rule Detection**:
   Antigravity will automatically detect `GEMINI.md` at the project root. All PMS extraction rules, forbidden characters, formatting guidelines, and sheet structures are immediately loaded into the agent's memory.
4. **Run Extractions**:
   Drop any new ship manual PDF into the folder (or Downloads), and simply prompt Antigravity:
   > *"Extract data for the new PDF manual in this folder following the PMS rules in GEMINI.md"*
5. **Verify**:
   Antigravity (or you) can run:
   ```bash
   python verify_pms_spares.py "SATHISH_<YOUR_FILE>.xlsx"
   ```

---

## Method 2: Using Any AI Assistant or Standalone Python on Another Computer

If Computer B does NOT have Antigravity:

1. **Install Python & Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Use `GEMINI.md` as System Prompt**:
   Copy the contents of `GEMINI.md` into your AI assistant (e.g. ChatGPT, Claude, Gemini Web, or API).
3. **Supply the Template**:
   Provide `TEMPLATE_PMS_SPARES.xlsx` to duplicate for each new PDF extraction.
4. **Run Verification**:
   ```bash
   python verify_pms_spares.py "SATHISH_<YOUR_FILE>.xlsx"
   ```

---

## How to Transfer the Files

You can transfer the zip archive `pms_spares_task_export.zip` via:
- **USB Flash Drive**
- **Google Drive / OneDrive / Dropbox**
- **Email attachment**
- **Git Repository** (GitHub / GitLab / Bitbucket)
