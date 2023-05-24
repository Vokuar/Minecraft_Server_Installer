import os
import string
import subprocess
import time
import shutil
import platform
import requests
import json
import pathlib

# Java server URLs
JAVA_SERVER_URLS = {
    "vanilla": "https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar",
    "Paper": lambda version: "https://api.papermc.io/v2/projects/paper/versions/{}/builds/{}/downloads/paper-{}-{}.jar".format(version, get_latest_build_number(version), version, get_latest_build_number(version)),
    "Forge": "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{}/forge-{}-installer.jar",
    "Fabric": "https://maven.fabricmc.net/net/fabricmc/fabric-server-launcher/{}/fabric-server-launcher-{}-universal.jar"
}

# Bedrock server URLs
BEDROCK_SERVER_URLS = {
    "Bedrock Dedicated Server": "https://dummy-bedrock-server-url.com/server.exe",
    "PocketMine": "https://dummy-pocketmine-server-url.com/server.phar",
    "Tesseract": "https://dummy-tesseract-server-url.com/server.zip",
    "BlueLight": "https://dummy-bluelight-server-url.com/server.jar",
    "Nukkit": "https://dummy-nukkit-server-url.com/server.jar",
}

def get_latest_build_number(version_number):
    url = f"https://papermc.io/api/v2/projects/paper/versions/{version_number}"

    response = requests.get(url)
    if not response.ok:
        raise ValueError(f"Failed to fetch Paper version details for {version_number}: {response.status_code} {response.reason}")

    data = json.loads(response.content)
    builds = data.get("builds")
    if not builds:
        raise ValueError(f"No builds found for Paper version {version_number}.")

    return builds

# Function to create a hidden folder
def hide_folder(path):
    """Hide the server directory."""
    if platform.system() == "Windows":
        try:
            import win32file
            win32file.SetFileAttributes(path, win32file.FILE_ATTRIBUTE_HIDDEN)
        except ImportError:
            choice = input("Unable to hide folder on Windows. Do you want to install pywin32? (y/n): ")
            if choice.lower() == "y":
                subprocess.run(["pip", "install", "pywin32"])
            else:
                print("Continuing without hiding the folder.")
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        try:
            subprocess.run(["chflags", "hidden", path])
        except subprocess.CalledProcessError:
            print("Unable to hide folder on macOS or Linux.")

# Function to install a Minecraft server
def install_server(server_name, server_type):
    # Get the user's home directory
    user_home = os.path.expanduser("~")

# Create the hidden directory and subdirectory if they do not exist
server_dir_name = ".Servers"
server_dir_path = pathlib.Path(user_home) / server_dir_name
if not server_dir_path.exists():
    server_dir_path.mkdir()
    hide_folder(str(server_dir_path))

    java_dir_path = server_dir_path / ".Java_servers"
    java_dir_path.mkdir()

    bedrock_dir_path = server_dir_path / ".Bedrock_servers"
    bedrock_dir_path.mkdir()
            
# Function to generate the server name based on user input and server type
def generate_server_name(server_name, server_type):
    return f"{server_name}_{server_type}_Server"

# Function to download a server file with retry logic
def download_server(url, file_path):
    max_attempts = 3
    attempt = 1
    while attempt <= max_attempts:
        print(f"Downloading server file from {url} (attempt {attempt})...")
        try:
            subprocess.run(["curl", "-o", file_path, url], check=True)
            print("Download complete.")
            return
        except subprocess.CalledProcessError:
            print("Download failed.")
            attempt += 1

    print(f"Failed to download server file from {url} after {max_attempts} attempts.")
    print(f"Please download it manually from {url}.")

# Function to check if an installation exists and prompt for reinstallation
def check_existing_installation(server_dir):
    if os.path.exists(server_dir):
        choice = input("An existing installation was found. Do you want to reinstall? (y/n): ")
        if choice.lower() == "y":
            print("Reinstalling...")
            shutil.rmtree(server_dir)
        else:
            print("Exiting.")
            exit(0)

# Function to accept the Minecraft EULA
def accept_eula(server_dir):
    eula_path = os.path.join(server_dir, "eula.txt")
    with open(eula_path, "w") as eula_file:
        eula_file.write("eula=true")

# Function to start the Minecraft server and wait for file generation
def start_server(server_file, server_dir):
    print("Starting server...")
    server_process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", server_file, "nogui"])
    time.sleep(10)

    # Wait for file generation
    print("Waiting for file generation...")
    while not os.path.exists(os.path.join(server_dir, "server.properties")) or not os.path.exists(os.path.join(server_dir, "eula.txt")):
        time.sleep(1)

    print("File generation complete.")

    # Stop the server if still running
    if server_process.poll() is None:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("Server terminated.")

# Function to install a Minecraft server
def install_server(server_name, server_type):
    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Generate the server name
    server_name = generate_server_name(server_name, server_type)

    # Set the server directory path
    server_dir = os.path.join(os.path.expanduser("~"), "." + server_name)

    # Check for an existing installation and prompt for reinstallation
    check_existing_installation(server_dir)

    # Create the server directory
    os.makedirs(server_dir, exist_ok=True)

    # Hide the server directory
    hide_folder(server_dir)

    # Determine the server file URL based on the server type
    if server_type == 1:  # Java server
        # Prompt for subcategory
        subcategory = int(input("Select the Java server subcategory:\n1. Vanilla\n2. Paper\n3. Forge\n4. Fabric\n"))

        server_url = JAVA_SERVER_URLS.get(list(JAVA_SERVER_URLS.keys())[subcategory-1])
        if not server_url:
            print("Invalid subcategory.")
            exit(1)

    elif server_type == 2:  # Bedrock server
        # Prompt for subcategory
        subcategory = int(input("Select the Bedrock server subcategory:\n1. Bedrock Dedicated Server\n2. PocketMine\n3. Tesseract\n4. BlueLight\n5. Nukkit\n"))

        server_url = BEDROCK_SERVER_URLS.get(list(BEDROCK_SERVER_URLS.keys())[subcategory-1])
        if not server_url:
            print("Invalid subcategory.")
            exit(1)

    else:
        print("Invalid server type.")
        exit(1)

    # Download the server file
    server_file = os.path.join(server_dir, "server.jar")
    download_server(server_url, server_file)

    # Additional setup steps or dependencies can be added here

    # Accept the Minecraft EULA
    accept_eula(server_dir)

    # Start the server
    start_server(server_file, server_dir)

    print("Minecraft server installation and setup completed.")
