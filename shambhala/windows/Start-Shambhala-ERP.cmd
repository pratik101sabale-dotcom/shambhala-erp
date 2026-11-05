@echo off
wsl -d Ubuntu-24.04 -u root --exec systemctl start erpnext-dev
if errorlevel 1 (
  echo Shambhala ERP could not start. Please share this error in the chat.
  pause
  exit /b 1
)
powershell.exe -NoProfile -NonInteractive -Command "Start-Process -FilePath 'C:\Windows\System32\wsl.exe' -WindowStyle Hidden -ArgumentList '-d','Ubuntu-24.04','-u','frappe','--exec','/bin/bash','/opt/erpnext-dev/keep-alive.sh'"
"%SystemRoot%\System32\curl.exe" --fail --silent --retry 15 --retry-connrefused --retry-delay 1 --retry-max-time 30 --max-time 3 "http://localhost:8000/api/method/ping" >nul 2>nul
if errorlevel 1 (
  echo Shambhala ERP is still starting. Open http://localhost:8000 after a few seconds.
  pause
  exit /b 1
)
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
  start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app="http://localhost:8000/desk"
  exit /b 0
)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app="http://localhost:8000/desk"
  exit /b 0
)
start "" "http://localhost:8000/desk"
