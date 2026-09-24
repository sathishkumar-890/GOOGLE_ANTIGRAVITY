@echo off
setlocal
echo ======================================================================
echo   Removing HLS Streaming Proxy Auto-Start from Windows Logon
echo ======================================================================

set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_SHORTCUT=%STARTUP_DIR%\HLS_Streaming_Proxy.lnk"

if exist "%TARGET_SHORTCUT%" (
    del "%TARGET_SHORTCUT%"
    echo [SUCCESS] Auto-start shortcut removed from Startup folder.
) else (
    echo [INFO] No auto-start shortcut found in Startup folder.
)

echo.
call "%~dp0stop_proxy.bat" --silent

echo ======================================================================
if "%1" neq "--silent" pause
