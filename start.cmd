@echo off

echo This script will download and install Python.
echo Python is required to run the Minecraft server installer script.
echo.

set /p download_python=Do you want to download and install Python? (y/n): 
if /i "%download_python%"=="y" (
    echo Downloading Python...
    wget https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -O python_installer.exe
    if not exist python_installer.exe (
        echo Failed to download Python installer. Exiting...
        exit /b 1
    )
    echo Python downloaded successfully.

    echo Installing Python...
    python_installer.exe /quiet Include_pip=1
    if not exist %USERPROFILE%\.python (
        echo Failed to install Python. Exiting...
        exit /b 1
    )
    echo Python installed successfully.
) else (
    echo Skipping Python installation.
)

echo.
echo Starting Minecraft server installer...
echo.

python minecraft_server_installer.py
