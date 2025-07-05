#!/data/data/com.termux/files/usr/bin/bash
# Termux Downloader Script (self-deleting)

REPO="https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main"
INSTALL_DIR="$HOME/minecraft-server"
MAIN_INSTALLER="$INSTALL_DIR/minecraft_server_manager.py"

# Install Python if needed
if ! command -v python3 >/dev/null; then
    echo "Installing Python..."
    pkg update -y
    pkg install python -y
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Download main installer
echo "Downloading Minecraft installer..."
curl -fsSL -o "$MAIN_INSTALLER" "$REPO/minecraft_server_manager.py"

# Make executable and run
chmod +x "$MAIN_INSTALLER"
python3 "$MAIN_INSTALLER"

# Self-destruct
echo "Cleaning up downloader..."
rm -f "$0"
echo "Downloader removed. Main installer kept at:"
echo "$MAIN_INSTALLER"
