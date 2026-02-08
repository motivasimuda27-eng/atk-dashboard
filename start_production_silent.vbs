' ATK Dashboard - Silent Production Starter (No Window)
' This VBScript runs the Python server without showing a console window

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check if pythonw.exe exists (no console window version)
pythonwCmd = "pythonw.exe"

' Run the waitress server in background without showing window
' 0 = Hide window completely
' True = Wait for command to complete (False = don't wait)
WshShell.Run """" & pythonwCmd & """ """ & scriptDir & "\waitress_server.py""", 0, False

' Show notification that server started
WshShell.Popup "ATK Dashboard Production Server started & vbCrLf & vbCrLf & "URL: http://127.0.0.1:5000" & vbCrLf & vbCrLf & "Use stop_production.bat to stop the server.", 5, "ATK Dashboard", 64
