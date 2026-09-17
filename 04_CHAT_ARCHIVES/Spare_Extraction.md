# Chat Archive: Spare_Extraction

- **Conversation ID**: 85f58c19-6ccb-4d88-8642-66f34445b4b5
- **Last Modified**: 2026-09-15 06:00:02.2944337+00:00
- **Total Messages**: 20

---

### 👤 User:
i have kept some files inside this directory can you analyse

### 🤖 Antigravity Agent:
I have started creating the Python virtual environment to inspect and validate the PMS Excel files using the project's verification tools. I will proceed with the analysis once this completes.

---

### 🤖 Antigravity Agent:
Waiting for virtual environment creation to finish...

---

### 🤖 Antigravity Agent:
Installing the required dependencies (`openpyxl`, `pypdf`, `pillow`) into the virtual environment...

---

### 🤖 Antigravity Agent:
Installation is almost finished. Waiting for completion...

---

### 🤖 Antigravity Agent:
### Overview of Directory Contents

This directory contains a complete, self-contained **Maritime Spare Parts Data Extraction & PMS Validation Environment** (extracted from `pms_spares_task_export.zip`). 

Its purpose is to extract spare parts, sub-assemblies, and consumables from ship technical manuals and drawings into an Excel template conforming strictly to ship **Planned Maintenance System (PMS)** formatting standards.

---

### File Inventory & Breakdown

| File Name | Type | Size | Description / Purpose |
| :--- | :--- | :--- | :--- |
| [`GEMINI.md`](file:///c:/Users/User/Documents/antigravity/joyful-turing/GEMINI.md) | Markdown / Rules | 4.7 KB | **System rules & extraction prompt**. Automatically loaded by Antigravity. Specifies all PMS formatting standards, character caps, forbidden characters, and sheet structures. |
| [`EXPORT_INSTRUCTIONS.md`](file:///c:/Users/User/Documents/antigravity/joyful-turing/EXPORT_INSTRUCTIONS.md) | Markdown | 3.0 KB | Guide on how to export, migrate, and run this extraction setup on other computers using Antigravity or standalone Python. |
| [`TEMPLATE_PMS_SPARES.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/TEMPLATE_PMS_SPARES.xlsx) | Excel Template | 61.2 KB | **Master Excel template** with 4 required sheets (`SPARES`, `Rules`, `Sheet2`, `Sheet3`) and pre-configured validation formulas in columns `V` through `AA` (rows 2 to 500). |
| [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) | Python Script | 5.5 KB | **Automated quality control validator**. Validates any PMS workbook against uppercase rules, forbidden characters, length limits, spacing rules, and formula integrity. |
| [`requirements.txt`](file:///c:/Users/User/Documents/antigravity/joyful-turing/requirements.txt) | Text | 47 B | Python dependencies: `openpyxl>=3.1.2`, `pypdf>=4.0.0`, `pillow>=10.0.0`. |
| [`SATHISH_BATTERY CHARGING BOARD FOR GENERAL USE.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_BATTERY%2
<truncated 1242 bytes>
AKUYO ELECTRONICS LTD.
   - **Drawing / Subsystem Code**: `RA1112-6072-1K`
   - **Subsystem Description**: `BUILT IN TYPE CBT ODC-3780-1K (RA1112-6072-1K)`
   - **Populated Data Rows**: 137 items (Handsets, cords, flush plates, transmitter/receiver units, headsets, and master telephone unit).

3. **`SATHISH_FLOAT FREE EPIRB.pdf.xlsx`**:
   - **Maker**: JAPAN RADIO CO., LTD.
   - **Drawing / Subsystem Code**: `2TE-5542`
   - **Subsystem Description**: `FLOAT FREE EPIRB JQE-103 (2TE-5542)`
   - **Populated Data Rows**: 30 items (Antenna, indicator lamp, stoppers, release bracket, battery unit, and master EPIRB assembly).

---

### Automated PMS Validation Results

We configured the Python virtual environment and ran [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) across all workbooks:

| File | Populated Rows | Validation Status | Formula Checks (V-AA down to 500) |
| :--- | :---: | :---: | :---: |
| `TEMPLATE_PMS_SPARES.xlsx` | 0 | **PASSED (0 errors)** | Intact |
| `SATHISH_BATTERY CHARGING BOARD...xlsx` | 14 | **PASSED (0 errors)** | Intact |
| `SATHISH_COMMON BATTERY TELEPHONE...xlsx` | 137 | **PASSED (0 errors)** | Intact |
| `SATHISH_FLOAT FREE EPIRB...xlsx` | 30 | **PASSED (0 errors)** | Intact |

All files strictly comply with:
- 100% Uppercase text.
- Length caps (Subsystem Description $\le$ 60 chars, Item Code $\le$ 25 chars, Short Description $\le$ 60 chars).
- No forbidden characters (`%`, `⌀`, `"`, `~`, `*`, `?`).
- Proper punctuation spacing (single space after commas, no spaces around hyphens or slashes).
- Inclusion of complete master assemblies with Position No `None` and quantity `1 SET`.

---

### Current Status & Next Steps

The workspace is ready for processing new ship technical manuals. 

If you have a new PDF manual to extract (for example, the manual found in your Downloads: `STERN TUBE SEALING - INTERMEDIATE SHAFT BEARING.pdf` or any other file), let me know and I will extract the parts and generate the verified PMS Excel workbook.

---

### 👤 User:
extract data for the new pdf manual in this folder following the pms rules in GEMINI.md

### 🤖 Antigravity Agent:
I have analyzed [Control Valve Manual.pdf](file:///c:/Users/User/Documents/antigravity/joyful-turing/Control%20Valve%20Manual.pdf) and prepared the implementation plan:

Please review the plan in [`implementation_plan.md`](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/implementation_plan.md). 

Once approved, I will proceed with generating the workbook [`SATHISH_Control Valve Manual.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_Control%20Valve%20Manual.pdf.xlsx) and validating it against all PMS rules.

---

### 🤖 Antigravity Agent:
The spare parts data from [Control Valve Manual.pdf](file:///c:/Users/User/Documents/antigravity/joyful-turing/Control%20Valve%20Manual.pdf) has been extracted and validated into [`SATHISH_Control Valve Manual.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_Control%20Valve%20Manual.pdf.xlsx) adhering strictly to the PMS rules in [`GEMINI.md`](file:///c:/Users/User/Documents/antigravity/joyful-turing/GEMINI.md).

### Summary of Extraction Results

- **Output Workbook**: [`SATHISH_Control Valve Manual.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_Control%20Valve%20Manual.pdf.xlsx)
- **Manufacturer**: `BY CONTROLS, INC.`
- **System Description**: `CONTROL VALVE`
- **Total Extracted Spares & Assemblies**: **269 items** across rows 2 through 270.
- **Figures & Assemblies Covered**:
  - **2-Way Control Valves**: DP Series & DG Series Direct and Reverse Acting (`Fig. 4`, `Fig. 5`, `Fig. 6`, `Fig. 7`).
  - **Diaphragm Actuators**: Direct and Reverse Acting Actuator assemblies (`Fig. 8`, `Fig. 9`).
  - **Top Mounted Hand Operating Devices (HOD)**: Direct and Reverse Acting (`Fig. 10`, `Fig. 11`).
  - **3-Way Rotary Control Valves**: Sizes 100A–150A, 200A–450A, and 500A–600A (`Fig. 16`, `Fig. 17`, `Fig. 18`).
  - **3-Way Globe Control Valves**: Sizes 25A, 40A–100A, and 125A–150A (`Fig. 21`, `Fig. 22`, `Fig. 23`).
  - **Master Complete Item**: Complete valve and actuator assembly (`PAGE.01`).

### Quality Control & PMS Validation

Ran [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) directly on the generated file:

```text
=== Verifying SATHISH_Control Valve Manual.pdf.xlsx ===
[OK] All 4 sheets present.
Total populated data rows: 269
[OK] ALL PMS VALIDATION RULES PASSED WITH 0 ERRORS!
```

- **100% Uppercase**: Verified across all columns.
- **Character Length Limits**: All descriptions and codes within PMS thresholds (Subsystem Description $\le$ 60, Item Code $\le$ 25, Short Description $\le$ 60).
- **Forbidden Characters**: Zero occurrences of `%`, `⌀`, `"`, `~`, `*`, or `?`.
- **Parentheses Compliance**: Parentheses used exclusively for drawing references at the end of Subsystem Descriptions; replaced with hyphens in descriptions.
- **Preserved Structure & Formulas**: All 4 sheets (`SPARES`, `Rules`, `Sheet2`, `Sheet3`) intact, with validation formulas in columns `V` through `AA` preserved down to row 500.

Detailed figure breakdowns and validation notes are available in the [Walkthrough Artifact](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/walkthrough.md).

---

### 👤 User:
extract data for the new pdf manual in this folder following the pms rules in GEMINI.md

### 🤖 Antigravity Agent:
Installing `pypdfium2` to render PDF drawings for visual verification...

---

### 🤖 Antigravity Agent:
I have analyzed [TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf](file:///c:/Users/User/Documents/antigravity/joyful-turing/TC01,%20TC02,%20TC03%20Temp.%20Regulating%20Valve%20Manaul%202.pdf) and prepared the implementation plan:

Please review the plan in [`implementation_plan.md`](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/implementation_plan.md).

Once approved, I will generate the workbook [`SATHISH_TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_TC01,%20TC02,%20TC03%20Temp.%20Regulating%20Valve%20Manaul%202.pdf.xlsx) and validate it against all PMS rules.

---

### 🤖 Antigravity Agent:
The data extraction from [TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf](file:///c:/Users/User/Documents/antigravity/joyful-turing/TC01,%20TC02,%20TC03%20Temp.%20Regulating%20Valve%20Manaul%202.pdf) has been completed and fully verified into [`SATHISH_TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_TC01,%20TC02,%20TC03%20Temp.%20Regulating%20Valve%20Manaul%202.pdf.xlsx) conforming strictly to the PMS rules in [`GEMINI.md`](file:///c:/Users/User/Documents/antigravity/joyful-turing/GEMINI.md).

### Summary of Extraction Results

- **Output Workbook**: [`SATHISH_TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_TC01,%20TC02,%20TC03%20Temp.%20Regulating%20Valve%20Manaul%202.pdf.xlsx)
- **Manufacturer**: `BY CONTROLS, INC.`
- **System Description**: `TEMPERATURE REGULATING VALVE`
- **Total Populated Spare Parts & Assemblies**: **62 rows** (Rows 2 to 63)
- **Equipment & Subsystem Scope**:
  - **Model TC01** (Steam Service, Direct Acting, Table 5 / Fig. 6): 15 component items (Body, Bonnet, Seat, Disc, Cap, Stem, Disc Holder, Packing, Gasket, Screen, Spring, Gland, Set Screw, Sensor Ass'y, Sensor Pocket) + 1 complete TC01 unit assembly.
  - **Model TC02** (Steam Service, Pilot Operated / Piston Type, Table 6 / Fig. 6): 23 component items (Body, Bonnet, Seat, Disc, Packing, Gasket, Spring, Top Cover, Cover, Pilot Plug, Pilot Seat, Pilot Gasket, Cylinder, Piston, Bottom Cover, Bolts, Bottom Gasket, Plug, Stud Bolt, Nut, Sensor Ass'y, Pocket) + 1 complete TC02 unit assembly.
  - **Model TC03** (Thermal Oil Service, Bellows Sealed, Table 7 / Fig. 6): 17 component items (Body, Bonnet, Seat, Disc, Cap, Stem, Disc Holder, Packing, Gasket, Spring, Gland, Cover, Gasket, Bolt, Bellows Ass'y, Sensor Ass'y, Sensor Pocket) + 1 complete TC03 unit assembly.
  - **TCS01 Sensor Sub-assembly** (Fig. 6 / Table 1): Sensor Assembly, Sensor Pocket Thermowell + 1 complete TCS01 unit.
  - **Master Complete Equipment Item**: `TC-SERIES` complete temperature regulating valves set (`PAGE 1`).

---

### Quality Control & PMS Validation

Executed [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) directly on the generated file:

```text
=== Verifying SATHISH_TC01, TC02, TC03 Temp. Regulating Valve Manaul 2.pdf.xlsx ===
[OK] All 4 sheets present.
Total populated data rows: 62
[OK] ALL PMS VALIDATION RULES PASSED WITH 0 ERRORS!
```

- **100% Uppercase**: Strictly enforced across all columns.
- **Length Caps**: Subsystem Description $\le$ 60 chars, Item Code $\le$ 25 chars, Short Description $\le$ 60 chars.
- **Zero Forbidden Characters**: No `%`, `⌀`, `"`, `~`, `*`, or `?`.
- **Parentheses Compliance**: Only at the end of Subsystem Descriptions; hyphens used in short and long descriptions.
- **Spacing & Punctuation**: Single space after commas; no spaces around hyphens or slashes.
- **Template & Formula Integrity**: All 4 sheets (`SPARES`, `Rules`, `Sheet2`, `Sheet3`) intact with formula columns `V` through `AA` preserved across all 500 rows.

A detailed summary is recorded in the [Walkthrough Document](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/walkthrough.md).

---

### 👤 User:
i have kept new template file for spare extraction use this upcoming manuals also refer all the sheets for rules and regulations, previously completed one manual for extraction you kept model as drawing number if there is no drawing number keep empty and for the system code there are rules behind if there is no drawing number take table number or else take chapter number or else take pdf page number refer all the rules for new template.

### 🤖 Antigravity Agent:
I have thoroughly reviewed and registered the new master template **[`Spare Template_13_09_2026_WISDOM.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/Spare%20Template_13_09_2026_WISDOM.xlsx)** along with all the rules across sheets `Spares`, `Rules`, `Sheet2`, and `Sheet3`.

---

### Key Extraction & Formatting Rules Adopted

1. **Draw No (Column P)**:
   - **Strict Rule**: If there is no explicit drawing number in the manual, Column P will be **left completely empty (`None` / blank)**.
   - We will **never** populate Column P with the equipment model name or figure number.

2. **Subsystem Code (Column H — Max 8 Characters)**:
   - Evaluated strictly using the 5-step fallback hierarchy:
     1. **Priority 1**: Drawing Number / Figure Number (`FIG.XX`) — *Always take the main drawing number*.
     2. **Priority 2**: If no drawing / figure number $\rightarrow$ **Table Number** (`TABLEXX`).
     3. **Priority 3**: If no table number $\rightarrow$ **Section Number** (`SEC.XX`).
     4. **Priority 4**: If no section number $\rightarrow$ **Chapter Number** (`CHAPT.XX.XX`).
     5. **Priority 5**: If no chapter number $\rightarrow$ **PDF Page Number** (`PG.XX.XX`).

3. **Subsystem Description (Column I — Max 60 Characters)**:
   - Format: `MACHINERY NAME MODEL (REF)` where `(REF)` matches the Subsystem Code / reference inside parentheses at the end.

4. **Item Code (Column J — Max 25 Characters)**:
   - **Priority 1**: Part Number, Code Number, Article Number, Type Number, Order Number, Item Number, Product Number, Catalog Number (exact).
   - **Priority 2**: If Item Code is absent and Model/Type exists $\rightarrow$ Model/Type.
   - **Priority 3**: If Item Code is absent $\rightarrow$ `POS/DRW_NO` or `POS/SUBSYSTEM_CODE`.
   - **Priority 4**: Drawing Position Number alone.

5. **Item Short Description (Column K — Max 60 Characters)**:
   - Spare part name **ONLY**.
   - No dimensions, voltages, wattage, weight, diameter, or specifications.
   - **No parentheses** (replace with hyphens).

6. **Item Long Description (Column L — Max 2000 Characters)**:
   - Comprehensive technical details (material, size, ratings, pressure, temperature, specs).
   - Symbol replacements: `%` $\rightarrow$ `PERCENTAGE`, `⌀` $\rightarrow$ `DIAMETER`, `"` $\rightarrow$ `INCH`, `~` $\rightarrow$ `-`, `&` $\rightarrow$ `AND`, `+` $\rightarrow$ `PLUS`, `-` $\rightarrow$ `MINUS`, `#` $\rightarrow$ `NO.`, `m²` $\rightarrow$ `M2`, `m³` $\rightarrow$ `M3`.
   - Hyphen instead of `( () — ” ' : ; @ )`.
   - Spacing: Single space after comma, no space around hyphens/slashes, single space before/after `X`.

7. **Master Equipment & Sub-Assemblies**:
   - Master complete equipment item included with Position `None`, Qty `1 SET`.
   - Major sub-units/modules included with Position `None`.

8. **Quantity (Column S)**:
   - Working Quantity only. If quantities differ by model, record model-wise breakdown in Long Description. If quantity is unavailable, leave blank.

9. **Exclusions**:
   - Do **NOT** extract `NAME PLATE`, `SPARE PART BOX`, or `SPARE PART TOOL BOX`.
   - Spares in non-English languages are excluded.

10. **Template Integrity & Validation**:
    - Formulas in Columns `V` through `AA` are preserved from Row 2 down to Row 500.
    - Updated [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) to validate both `Spares` and `SPARES` sheets, including strict Subsystem Code length checks ($\le 8$ characters).

---

### Ready for Next Manual
Please place the next manual PDF into the workspace folder or let me know which manual to extract next.

---

### 👤 User:
how to ask data extraction for next manual

### 🤖 Antigravity Agent:
To request data extraction for your next manual, you can follow this simple process:

---

### Step 1: Place the Manual in the Workspace Folder
Copy or drop your PDF manual file into the project folder:
📁 `c:\Users\User\Documents\antigravity\joyful-turing`

---

### Step 2: Send a Message in Chat
You can simply send any of the following message formats:

#### Option A: Quick & Simple (Most Common)
> *"I have added `[Manual Name].pdf` into the folder. Please extract the spare parts using the new template."*

#### Option B: Minimal Prompt
> *"Extract data for the new PDF manual in this folder."*

#### Option C: With Specific Equipment Details (If available)
If you have specific vessel PMS codes or details from your allocation list, you can provide them:
> *"Please extract `[Manual Name].pdf` using the new template with the following details:*
> - *Location Code / Description: [e.g., E01 / ENGINE ROOM]*
> - *System Code / Description: [e.g., 601.001 / AUXILIARY ENGINE]*
> - *Maker: [e.g., YANMAR]*
> - *Vessel Installed Qty: [e.g., 2 SETS]"*

*(Note: If you don't provide these, I will automatically identify the Maker, Model, drawings, and working quantities directly from the manual).*

---

### What Happens Automatically:
1. **Reads All Spares**: Parses all drawings, section views, parts lists, and periodic maintenance tables.
2. **Uses Master Template**: Populates [`Spare Template_13_09_2026_WISDOM.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/Spare%20Template_13_09_2026_WISDOM.xlsx) preserving all formulas in columns `V`–`AA`.
3. **Applies All Strict Rules**:
   - Empty `Draw No` (Column P) when no explicit drawing number exists.
   - Subsystem Code hierarchy (`FIG.XX` $\rightarrow$ `TABLEXX` $\rightarrow$ `SEC.XX` $\rightarrow$ `CHAPT.XX.XX` $\rightarrow$ `PG.XX.XX`).
   - 100% UPPERCASE, character length limits, and forbidden symbol replacements.
   - Master equipment item and major sub-assemblies included with Position `None`.
4. **Validates Quality**: Automatically runs [`verify_pms_spares.py`](file:///c:/Users/User/Documents/antigravity/joyful-turing/verify_pms_spares.py) to guarantee **0 errors**.
5. **Generates Output File**: Delivers `SATHISH_<Manual Name>.xlsx`.

---

### 👤 User:
Extract data for the new PDF manual in this folder.

### 🤖 Antigravity Agent:
I have completed the thorough analysis of [`F-34 ACCOMMODATION LADDER.pdf`](file:///c:/Users/User/Documents/antigravity/joyful-turing/F-34%20ACCOMMODATION%20LADDER.pdf) and prepared the technical extraction plan.

Please review the [Implementation Plan](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/implementation_plan.md) for details on:
- Equipment & subsystem breakdown (`AIR WINCH`, `AIR MOTOR`, `OILER & FILTER`, `ACCOMMODATION LADDER`, `FALL ARREST`, `LIFE NET`, etc.)
- Strict application of the new template rules (empty `Draw No` when absent, 5-level `Subsystem Code` hierarchy, Item Code priorities, text formatting, and formula preservation)
- Explicit exclusion of `SPARE BOX` and `NAME PLATE` per PMS regulations

Please let me know if you approve this plan or if you would like any adjustments before I proceed to extract the data and generate `SATHISH_F-34 ACCOMMODATION LADDER.pdf.xlsx`.

---

### 🤖 Antigravity Agent:
The spare parts extraction for **`F-34 ACCOMMODATION LADDER.pdf`** is complete.

The output workbook **[`SATHISH_F-34 ACCOMMODATION LADDER.pdf.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/SATHISH_F-34%20ACCOMMODATION%20LADDER.pdf.xlsx)** has been generated using the new master template **[`Spare Template_13_09_2026_WISDOM.xlsx`](file:///c:/Users/User/Documents/antigravity/joyful-turing/Spare%20Template_13_09_2026_WISDOM.xlsx)** and verified with **0 PMS validation errors**.

Please see the [Walkthrough](file:///C:/Users/User/.gemini/antigravity/brain/85f58c19-6ccb-4d88-8642-66f34445b4b5/walkthrough.md) for full subsystem details, row counts, and validation results.

### Summary Highlights
- **261 total spare rows** populated across 20 distinct equipment assemblies and drawings (`AIR WINCH`, `AIR MOTOR`, `OILER & FILTER`, `ACCOMMODATION LADDER`, `FALL ARREST`, `LIFE NET`, `TURN TABLE`, `UPPER PLATFORM`, `DAVITS`, `WINCH SEAT`, `LADDER REST`, etc.).
- **Draw No (Column P)**: Left completely empty (`None` / blank) for entries where no authentic drawing number exists (such as Table 04 and Table 38).
- **Subsystem Code Hierarchy (Column H)**: Applied strictly ($\le 8$ characters) prioritizing Drawing prefixes (`OTW-1320`, `OTM-4.5P`, `AC-STD-O`, `AC-VET-L`, `18J010-L`, `18J010-S`, `AC-STD-S`, `AC-STD-W`, `AC-VET-R`) and falling back to Table numbers (`TABLE04`, `TABLE38`).
- **Exclusions**: `NAME PLATE` and `SPARE BOX` strictly excluded per PMS rules.
- **Formula & Sheet Integrity**: All 4 sheets preserved (`Spares`, `Rules`, `Sheet2`, `Sheet3`), with formulas in columns `V` through `AA` intact down to row 500.

---

