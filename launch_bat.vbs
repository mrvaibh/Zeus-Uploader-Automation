Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "<ABSOLUTE_PATH_TO_DIR>\script.bat" & Chr(34), 0
Set WshShell = Nothing