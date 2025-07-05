@echo off
:: Windows Downloader Script (self-deleting)

set REPO=https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main
set INSTALL_DIR=%USERPROFILE%\minecraft-server
set MAIN_INSTALLER=%INSTALL_DIR%\minecraft_server_installer.py

:: Install Python if needed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Python...
    winget install Python.Python.3 -e >nul || (
        echo Please install Python manually: https://www.python.org/downloads/
        exit /b 1
    )
)

:: Create installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Download main installer
echo Downloading Minecraft installer...
curl -fsSL -o "%MAIN_INSTALLER%" "%REPO%/minecraft_server_installer.py" || (
    echo Download failed
    exit /b 1
)

:: Run main installer
python "%MAIN_INSTALLER%"

:: Self-destruct
echo Cleaning up downloader...
del /f /q "%~f0"
echo Downloader removed. Main installer kept at:
echo %MAIN_INSTALLER%
pause
