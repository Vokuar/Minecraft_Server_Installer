import os
import random
import string
import platform
import subprocess
import time

# Function to generate a random alphanumeric name
def generate_random_name(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to download a server file
def download_server(url, file_path):
    try:
        subprocess.run(["curl", "-o", file_path, url], check=True)
    except subprocess.CalledProcessError:
        print("Failed to download the server file.")
        exit(1)

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

    # Stop the server
    print("Stopping server...")
    server_process.terminate()
    server_process.wait()
    print("Server terminated.")

# Function to install a Minecraft server
def install_server(server_type):
    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Generate a random name for the server folder
    server_name = generate_random_name(8)

    # Set the server directory path
    server_dir = os.path.join(user_home, f".{server_name}_{server_type}_server")

    # Check for an existing installation and prompt for reinstallation
    check_existing_installation(server_dir)

    # Create the server directory
    os.makedirs(server_dir, exist_ok=True)

    # Download the server file based on the server type
    if server_type == "java":
        server_url = "https://dummy-java-server-url.com/server.jar"
    elif server_type == "bedrock":
        server_url = "https://dummy-bedrock-server-url.com/server.exe"
    else:
        print("Invalid server type.")
        exit(1)

    server_file = os.path.join(server_dir, "server.jar")
    download_server(server_url, server_file)

    # Install additional dependencies or perform any other setup steps here

    # Accept the Minecraft EULA
    accept_eula(server_dir)

    # Start the server and wait for file generation
    start_server(server_file)

    print("Minecraft server installation and setup completed.")

# Main program
def main():
    # Prompt for server type
    print("Choose a server type:")
    print("1. Java")
    print("2. Bedrock")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        server_type = "java"
    elif choice == "2":
        server_type = "bedrock"
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    # Install the Minecraft server
    install_server(server_type)

# Run the main program
if __name__ == "__main__":
    main()
