@echo off

echo This script will download and install Python.
echo Python is required to run the Minecraft server installer script.
echo.

set /p "install_python=Do you want to download and install Python? (y/n): "
if /i "%install_python%"=="y" (
    echo Checking if Python is already installed...

    REM Check if Python is already installed
    if exist "%ProgramFiles%\Python39\python.exe" (
        echo Python is already installed.
    ) else (
        echo Python is not installed.

        REM Check if Chocolatey is installed
        choco -v >nul 2>&1
        if %errorlevel% equ 0 (
            echo Chocolatey is already installed.
        ) else (
            echo Chocolatey is not installed.

            set /p "install_chocolatey=Do you want to download and install Chocolatey? (y/n): "
            if /i "%install_chocolatey%"=="y" (
                echo Downloading Chocolatey installer...
                powershell -Command "wget https://chocolatey.org/install.ps1 -OutFile chocolatey_installer.ps1"

                echo Installing Chocolatey...
                powershell -ExecutionPolicy Bypass -NoProfile -File chocolatey_installer.ps1

                echo.
                echo Chocolatey installed successfully.
            ) else (
                echo Skipping Chocolatey installation.
                echo If you want to install Chocolatey manually, you can visit the Chocolatey website at:
                echo https://chocolatey.org/
            )
        )

        echo.
        echo Checking if Chocolatey is installed...

        REM Check if Chocolatey is installed
        choco -v >nul 2>&1
        if %errorlevel% equ 0 (
            echo Chocolatey is installed. Attempting to install Python using Chocolatey...
            choco install python -y
        ) else (
            echo Chocolatey is not installed. Falling back to web download method.

            echo.
            echo Downloading Python installer from python.org...
            powershell -Command "wget https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe -OutFile python_installer.msi"

            echo.
            echo Installing Python...
            python_installer.msi /quiet PrependPath=1

            echo.
            echo Python installed successfully.
        )
    )
) else (
    echo Skipping Python installation.
    echo If you want to install Python manually, you can visit the Python website at:
    echo https://www.python.org/downloads/
)

echo.
echo Starting Minecraft server installer...
echo.

python minecraft_server_installer.py

