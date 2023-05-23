#!/data/data/com.termux/files/usr/bin/bash
#!/bin/bash

# Check if Python is installed
command -v python >/dev/null 2>&1 || {
    echo "Python is not installed. Please install Python and re-run the script."
    read -n 1 -s -r -p "Press any key to continue..."
    exit 1
}

# Run the Python script
python minecraft_server_installer.py

read -n 1 -s -r -p "Press any key to exit..."
