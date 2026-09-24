' Silent Background Launcher for Multi-Stream HLS Proxy
' Runs pythonw.exe with window style 0 (completely hidden, zero popup)

Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetAbsolutePathName(fso.GetParentFolderName(WScript.ScriptFullName))
proxyScript = currentDir & "\multi_stream_proxy.py"

Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = currentDir
WshShell.Run "pythonw.exe """ & proxyScript & """", 0, False
