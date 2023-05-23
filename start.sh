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
            sudo apt install python3 -y
        elif command -v yum >/dev/null 2>&1; then
            echo "Installing Python using yum..."
            sudo yum update
            sudo yum install python3 -y
        else
            echo "Unable to determine the package manager. Falling back to manual installation..."
            
            # Download Python from the web
            echo "Downloading Python..."
            wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz -O python.tar.xz
            if [ ! -f python.tar.xz ]; then
                echo "Failed to download Python. Exiting..."
                exit 1
            fi
            echo "Python downloaded successfully."

            echo "Installing Python..."
            tar -xf python.tar.xz
            cd Python-3.10.0
            ./configure --prefix=$HOME/.python
            make -j$(nproc)
            make install
            cd ..
            if [ ! -d $HOME/.python ]; then
                echo "Failed to install Python. Exiting..."
                exit 1
            fi
            echo "Python installed successfully."
        fi
    fi
else
    echo "Skipping Python installation."
fi

echo
echo "Starting Minecraft server installer..."
echo

python3 minecraft_server_installer.py
