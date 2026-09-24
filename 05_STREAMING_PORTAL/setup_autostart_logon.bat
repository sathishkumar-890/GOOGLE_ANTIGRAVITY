@echo off
setlocal
echo ======================================================================
echo   Configuring HLS Streaming Proxy Auto-Start on Windows Logon
echo ======================================================================

set "SCRIPT_DIR=%~dp0"
set "VBS_PATH=%SCRIPT_DIR%start_silent.vbs"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_SHORTCUT=%STARTUP_DIR%\HLS_Streaming_Proxy.lnk"

echo Script Path: %VBS_PATH%
echo Startup Folder: %STARTUP_DIR%

if not exist "%VBS_PATH%" (
    echo [ERROR] Could not find start_silent.vbs in %SCRIPT_DIR%
    pause
    exit /b 1
)

:: Create Windows Shortcut in Startup Folder using PowerShell
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; " ^
  "$s = $ws.CreateShortcut('%TARGET_SHORTCUT%'); " ^
  "$s.TargetPath = 'wscript.exe'; " ^
  "$s.Arguments = '\"%VBS_PATH%\"'; " ^
  "$s.WorkingDirectory = '%SCRIPT_DIR%'; " ^
  "$s.WindowStyle = 7; " ^
  "$s.Save()"

if exist "%TARGET_SHORTCUT%" (
    echo.
    echo [SUCCESS] Auto-start configured!
    echo Shortcut created: %TARGET_SHORTCUT%
    echo.
    echo Starting the HLS Proxy silently right now...
    wscript.exe "%VBS_PATH%"
    powershell -NoProfile -Command "Start-Sleep -Seconds 2"
    echo.
    echo Testing connection to http://localhost:8888/api/channels ...
    powershell -NoProfile -Command "try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8888/api/channels' -TimeoutSec 3; Write-Host ('[OK] Proxy is ACTIVE! Online Channels: ' + $r.count) } catch { Write-Host '[INFO] Proxy started in background.' }"
    echo.
    echo From now on, this proxy will automatically start silently every time you log on to Windows!
) else (
    echo [ERROR] Failed to create shortcut in Startup folder.
)

echo ======================================================================
if "%1" neq "--silent" pause
