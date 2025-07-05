#!/usr/bin/env sh
# Platform-agnostic launcher script
# Detects OS and downloads appropriate downloader script

REPO="https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main"

# Detect platform
detect_platform() {
    case "$(uname -s)" in
        Linux*)
            if [ -d "/data/data/com.termux/files/usr" ]; then
                echo "termux"
            else
                echo "linux"
            fi
            ;;
        Darwin*) echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# Download and execute platform-specific downloader
PLATFORM=$(detect_platform)
DOWNLOADER_URL="$REPO/downloader-$PLATFORM.sh"

echo "Detected platform: $PLATFORM"
echo "Downloading installer..."

if command -v curl >/dev/null; then
    curl -fsSL "$DOWNLOADER_URL" | sh
elif command -v wget >/dev/null; then
    wget -qO - "$DOWNLOADER_URL" | sh
else
    echo "ERROR: Need curl or wget to proceed"
    exit 1
fi
