/**
 * Enhanced IPTV Google Sheets Sync & Auto-Clean Webhook
 * 
 * Features:
 * 1. Supports multi-sheet operations via "sheetName": "IPTV_Playlist" or "Sheet2".
 * 2. 1-Click UI Menu inside Google Sheets ("📺 IPTV Tools" > "⚡ Clean & Deduplicate Sheet2").
 * 3. Formats headers (#1e293b) and status cells (Live = Green, Dead = Red).
 */

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('📺 IPTV Tools')
    .addItem('⚡ 1-Click Deduplicate & Format Sheet2', 'cleanAndFormatSheet2')
    .addToUi();
}

function doGet(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ContentService.createTextOutput(JSON.stringify({
    status: "online",
    spreadsheet: ss.getName(),
    sheets: ss.getSheets().map(function(s) { return s.getName(); })
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(15000);
  
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // Select target sheet by name, or fallback to active sheet
    var targetName = data.sheetName || data.sheet || "IPTV_Playlist";
    var sheet = ss.getSheetByName(targetName);
    if (!sheet) {
      sheet = ss.getActiveSheet();
    }
    
    // ACTION 1: Replace/Sync All Rows
    if (data.action === "sync_all") {
      var rows = data.rows; // 2D array: [["STREAM NAME", "URL", "CATEGORY", "ICON", "STATUS"], ...]
      if (rows && rows.length > 0) {
        sheet.clearContents();
        sheet.getRange(1, 1, rows.length, rows[0].length).setValues(rows);
        
        // Header styling
        sheet.getRange(1, 1, 1, rows[0].length)
             .setBackground("#1e293b")
             .setFontColor("#ffffff")
             .setFontWeight("bold");
        
        // Color-code Status column (Column 5 / E)
        for (var i = 1; i < rows.length; i++) {
          var statusCell = sheet.getRange(i + 1, 5);
          var val = String(rows[i][4]).trim();
          if (val === "Live") {
            statusCell.setBackground("#dcfce7").setFontColor("#15803d").setFontWeight("bold");
          } else if (val === "Dead") {
            statusCell.setBackground("#fee2e2").setFontColor("#b91c1c");
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        sheet: sheet.getName(),
        updatedRows: rows.length
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // ACTION 2: Update Statuses by URL matching
    if (data.action === "update_status") {
      var updates = data.updates; // Object: { "url": "Live", ... }
      var lastRow = sheet.getLastRow();
      var count = 0;
      if (lastRow > 1) {
        var urlRange = sheet.getRange(2, 2, lastRow - 1, 1).getValues();
        for (var i = 0; i < urlRange.length; i++) {
          var url = String(urlRange[i][0]).trim();
          if (updates.hasOwnProperty(url)) {
            var newStatus = updates[url];
            var statusCell = sheet.getRange(i + 2, 5);
            statusCell.setValue(newStatus);
            if (newStatus === "Live") {
              statusCell.setBackground("#dcfce7").setFontColor("#15803d").setFontWeight("bold");
            } else {
              statusCell.setBackground("#fee2e2").setFontColor("#b91c1c");
            }
            count++;
          }
        }
      }
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        sheet: sheet.getName(),
        updatedCount: count
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: "Unknown action"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

/**
 * Helper function for 1-click execution inside Google Sheets
 */
function cleanAndFormatSheet2() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Sheet2");
  if (!sheet) {
    SpreadsheetApp.getUi().alert("Sheet2 not found!");
    return;
  }
  
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  
  var data = sheet.getRange(2, 1, lastRow - 1, 5).getValues();
  var seen = {};
  var uniqueRows = [];
  
  for (var i = 0; i < data.length; i++) {
    var url = String(data[i][1]).trim();
    if (url && !seen[url]) {
      seen[url] = true;
      uniqueRows.append(data[i]);
    }
  }
  
  sheet.getRange(2, 1, lastRow - 1, 5).clearContent();
  sheet.getRange(2, 1, uniqueRows.length, 5).setValues(uniqueRows);
  
  // Format
  for (var j = 0; j < uniqueRows.length; j++) {
    var cell = sheet.getRange(j + 2, 5);
    var status = String(uniqueRows[j][4]).trim();
    if (status === "Live") {
      cell.setBackground("#dcfce7").setFontColor("#15803d").setFontWeight("bold");
    } else if (status === "Dead") {
      cell.setBackground("#fee2e2").setFontColor("#b91c1c");
    }
  }
  
  SpreadsheetApp.getUi().alert("Sheet2 cleaned! Duplicates removed. Unique rows: " + uniqueRows.length);
}
