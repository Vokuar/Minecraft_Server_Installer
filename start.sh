#!/data/data/com.termux/files/usr/bin/bash
#!/bin/bash

echo "This script will download and install Python."
echo "Python is required to run the Minecraft server installer script."
echo

read -p "Do you want to download and install Python? (y/n): " download_python
if [[ $download_python == [Yy] ]]; then
    echo "Checking if Python is already installed..."

    # Check if Python is already installed using the package manager
    if command -v python3 >/dev/null 2>&1; then
        echo "Python is already installed."
    else
        echo "Python is not installed. Attempting to install using the package manager..."
        
        # Install Python using the package manager (apt, yum, etc.)
        if command -v apt >/dev/null 2>&1; then
            echo "Installing Python using apt..."
            sudo apt update
