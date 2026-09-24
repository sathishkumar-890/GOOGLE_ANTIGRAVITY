@echo off
set PORT=8888
echo Stopping HLS Streaming Proxy on port %PORT%...
powershell -NoProfile -Command "$conn = Get-NetTCPConnection -LocalPort %PORT% -ErrorAction SilentlyContinue; if ($conn) { foreach ($c in $conn) { Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue; Write-Host ('Stopped Proxy PID: ' + $c.OwningProcess) } Write-Host 'HLS Proxy stopped successfully.' } else { Write-Host 'No proxy process running on port %PORT%.' }"
if "%1" neq "--silent" pause
