/**
 * ⚡ 1-CLICK INSTANT GOOGLE APPS SCRIPT: REMOVE GREEN HIGHLIGHT FROM LIVE STATUS
 * 
 * Target Spreadsheet:
 * https://docs.google.com/spreadsheets/d/1YGz5cSLqtTw9tnHAjiNHLoT3__DHCLHcyMiGF6ElRBc/edit
 * 
 * HOW TO RUN (Takes 5 seconds):
 * 1. Open your Google Spreadsheet in your browser.
 * 2. Click 'Extensions' > 'Apps Script' in the top menu.
 * 3. Copy and paste this entire code into the code editor (replacing or adding to existing code).
 * 4. Select 'removeLiveGreenHighlight' from the function dropdown at the top, then click 'Run' (▶).
 * 
 * WHAT THIS DOES:
 * - Scans all sheets ('IPTV_Playlist', 'Sheet2', 'IPTV', etc.).
 * - Removes the green background (#dcfce7 / green fill) from every "Live" status cell.
 * - Resets "Live" cells to clean, standard styling: no background fill, regular black font.
 * - Removes any conditional formatting rules that color "Live" cells green.
 * - Keeps dark headers (#1e293b) and any dead status styling untouched.
 */

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('📺 IPTV Tools')
    .addItem('🧹 Remove Green Highlight from Live Status', 'removeLiveGreenHighlight')
    .addToUi();
}

function removeLiveGreenHighlight() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  var totalCleared = 0;
  var report = [];

  for (var s = 0; s < sheets.length; s++) {
    var sheet = sheets[s];
    var sheetName = sheet.getName();
    var lastRow = sheet.getLastRow();
    var lastCol = sheet.getLastColumn();
    
    if (lastRow < 2) continue;

    var sheetClearedCount = 0;

    // 1. Remove conditional formatting rules that color "Live" green
    var rules = sheet.getConditionalFormatRules();
    var keptRules = [];
    for (var r = 0; r < rules.length; r++) {
      var rule = rules[r];
      var boolCond = rule.getBooleanCondition();
      var isLiveRule = false;
      if (boolCond) {
        var criteria = boolCond.getCriteriaValues();
        if (criteria && criteria.length > 0) {
          for (var c = 0; c < criteria.length; c++) {
            if (String(criteria[c]).toLowerCase().indexOf("live") !== -1) {
              isLiveRule = true;
              break;
            }
          }
        }
        var bg = boolCond.getBackground();
        if (bg && (bg.toLowerCase() === "#dcfce7" || bg.toLowerCase() === "#b7e1cd" || bg.toLowerCase() === "#00ff00")) {
          isLiveRule = true;
        }
      }
      if (!isLiveRule) {
        keptRules.push(rule);
      }
    }
    sheet.setConditionalFormatRules(keptRules);

    // 2. Scan Column E (Status column)
    var numRows = lastRow - 1;
    var statusRange = sheet.getRange(2, 5, numRows, 1);
    var values = statusRange.getValues();
    var backgrounds = statusRange.getBackgrounds();
    var fontColors = statusRange.getFontColors();
    var fontWeights = statusRange.getFontWeights();

    for (var i = 0; i < values.length; i++) {
      var val = String(values[i][0]).trim();
      var bg = String(backgrounds[i][0]).toLowerCase();

      // If status is Live or cell has green fill
      if (val.toLowerCase() === "live" || bg === "#dcfce7" || bg === "#b7e1cd") {
        backgrounds[i][0] = null;       // Remove background highlight completely
        fontColors[i][0] = "#000000";   // Standard clean black text
        fontWeights[i][0] = "normal";   // Regular weight (no bold green)
        sheetClearedCount++;
        totalCleared++;
      }
    }

    statusRange.setBackgrounds(backgrounds);
    statusRange.setFontColors(fontColors);
    statusRange.setFontWeights(fontWeights);

    report.push(sheetName + ": " + sheetClearedCount + " Live cells cleaned");
  }

  Logger.log("COMPLETED: Removed green highlight from " + totalCleared + " Live cells.");
  Logger.log(report.join("\n"));

  try {
    SpreadsheetApp.getUi().alert(
      "✅ Green Highlights Removed Successfully!\n\n" +
      "Cleaned " + totalCleared + " 'Live' status cells across all sheets.\n\n" +
      report.join("\n")
    );
  } catch (e) {
    // Non-UI execution
  }
}
