@echo off

REM Check if Python is installed
python --version 2>NUL
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and re-run the script.
    pause
    exit /b
)

REM Run the Python script
python minecraft_server_installer.py
pause
