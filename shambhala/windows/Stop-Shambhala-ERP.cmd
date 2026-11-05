@echo off
wsl -d Ubuntu-24.04 -u root --exec systemctl stop erpnext-dev
if errorlevel 1 (
  echo Shambhala ERP could not stop. Please share this error in the chat.
  pause
  exit /b 1
)
echo Shambhala ERP stopped.
