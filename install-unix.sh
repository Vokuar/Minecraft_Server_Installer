#!/bin/bash
# Unix Downloader Script (self-deleting)

REPO="https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main"
INSTALL_DIR="$HOME/minecraft-server"
MAIN_INSTALLER="$INSTALL_DIR/minecraft_server_installer.py"

# Install Python if needed
if ! command -v python3 >/dev/null; then
    echo "Installing Python..."
    
    if command -v apt >/dev/null; then
        sudo apt update -y
        sudo apt install python3 -y
    elif command -v yum >/dev/null; then
        sudo yum update -y
        sudo yum install python3 -y
    elif command -v brew >/dev/null; then
        brew install python
    else
        echo "ERROR: Couldn't install Python automatically"
        exit 1
    fi
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Download main installer
echo "Downloading Minecraft installer..."
if command -v curl >/dev/null; then
    curl -fsSL -o "$MAIN_INSTALLER" "$REPO/minecraft_server_installer.py"
else
    wget -q -O "$MAIN_INSTALLER" "$REPO/minecraft_server_installer.py"
fi

# Make executable and run
chmod +x "$MAIN_INSTALLER"
python3 "$MAIN_INSTALLER"

# Self-destruct
echo "Cleaning up downloader..."
rm -f "$0"
echo "Downloader removed. Main installer kept at:"
echo "$MAIN_INSTALLER"
