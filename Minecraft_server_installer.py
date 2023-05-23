import os
import string
import subprocess
import time
import shutil
import platform

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
def start_server(server_file):
    print("Starting server...")
    server_process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", server_file, "nogui"])
    time.sleep(10)

    # Wait for file generation
    print("Waiting for file generation...")
    while not os.path.exists("server.properties") or not os.path.exists("eula.txt"):
        time.sleep(1)

    print("File generation complete.")
    
    # Stop the server if still running
    if server_process.poll() is None:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("Server terminated.")

# Function to create a hidden folder
def hide_folder(path):
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

    # Generate the server name
    server_name = generate_server_name(server_name, server_type)

    # Set the server directory path
    server_dir = os.path.join(user_home, server_name)

        # Check for an existing installation and prompt for reinstallation
    check_existing_installation(server_dir)

    # Create the server directory
    os.makedirs(server_dir, exist_ok=True)

    # Hide the server directory
    hide_folder(server_dir)

    # Determine the server file URL based on the server type
    if server_type == "java":
        server_url = "https://dummy-java-server-url.com/server.jar"
    elif server_type == "bedrock":
        server_url = "https://dummy-bedrock-server-url.com/server.exe"
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
    start_server(server_file)

    print("Minecraft server installation and setup completed.")

# Main program
def main():
    # Get the server name from user input
    server_name = input("Enter the server name: ")

    # Set the server type based on the server file source
    server_type = "java"  # Replace with the logic to determine the server type based on the server file source

    # Install the Minecraft server
    install_server(server_name, server_type)

# Run the main program
if __name__ == "__main__":
    main()

