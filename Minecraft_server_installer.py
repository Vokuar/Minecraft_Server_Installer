import os
import random
import string
import subprocess

# Function to generate a random alphanumeric name
def generate_random_name(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to download a server file and retry on failure
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

    print(f"Failed to download server file from {url} after {max_attempts} attempts. Exiting.")
    exit(1)

# Function to check if an installation exists at the desired location
def check_existing_installation(server_dir):
    if os.path.exists(server_dir):
        choice = input(f"An existing installation was found at {server_dir}. Do you want to reinstall? (y/n): ")
        if choice.lower() != "y":
            print("Exiting.")
            exit(0)
        print("Reinstalling...")
        shutil.rmtree(server_dir)

# Function to accept the Minecraft EULA
def accept_eula(server_dir):
    eula_file = os.path.join(server_dir, "eula.txt")
    with open(eula_file, "w") as f:
        f.write("eula=true")

# Function to start the Minecraft server
def start_server(server_file):
    print("Starting server...")
    subprocess.run(["java", "-Xmx1024M", "-Xms1024M", "-jar", server_file, "nogui"])
    print("Server has started.")

# Function to wait for file generation
def wait_for_file_generation(server_dir):
    print("Waiting for file generation...")
    while not os.path.isfile(os.path.join(server_dir, "server.properties")) or \
          not os.path.isfile(os.path.join(server_dir, "eula.txt")):
        time.sleep(1)
    print("File generation complete.")

# Main program
def main():
    # Prompt for server type
    print("Choose a server type:")
    print("1. Java")
    print("2. Bedrock")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        server_type = "java"
        server_url = "https://dummy-java-server-url.com/server.jar"
    elif choice == "2":
        server_type = "bedrock"
        server_url = "https://dummy-bedrock-server-url.com/server.exe"
    else:
        print("Invalid choice.")
        exit(1)

    # Prompt for installation confirmation
    print(f"You have chosen to install a {server_type.capitalize()} server.")
    confirmation = input("Proceed with the installation? (y/n): ")

    if confirmation.lower() != "y":
        print("Installation cancelled.")
        exit(0)

    # Generate a random name for the server folder
    server_name = generate_random_name(8)

    # Set the server directory path
    user_home = os.path.expanduser("~")
    server_dir = os.path.join(user_home, f".{server_name}_{server_type}_server")

    # Check for an existing installation
    check_existing_installation(server_dir)

    # Create the server directory
    os.makedirs(server_dir, exist_ok=True)

    # Download the server file
    server_file     server_file = os.path.join(server_dir, "server.jar")
    download_server(server_url, server_file)
    
    # Accept the Minecraft EULA
    accept_eula(server_dir)
    
    # Start the Minecraft server
    start_server(server_file)
    
    # Wait for file generation
    wait_for_file_generation(server_dir)
    
    print("Minecraft server installation and setup complete.")

if __name__ == "__main__":
    main()

