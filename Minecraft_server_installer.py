import os
import random
import string
import platform
import subprocess

# Function to start the server
def start_server(server_file, server_type):
    if server_type == "java":
        subprocess.run(["java", "-Xmx2G", "-Xms1G", "-jar", server_file, "nogui"])
    elif server_type == "bedrock":
        subprocess.run(["./bedrock_server"])
    else:
        print("Invalid server type.")
        exit(1)

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

# Function to install a Minecraft server
def install_server(server_type):
    # Get the user's home directory
    user_home = os.path.expanduser("~")

    # Generate a random name for the server folder
    server_name = generate_random_name(8)

    # Set the server directory path
    server_dir = os.path.join(user_home, f".{server_name}_{server_type}_server")

    # Create the server directory
    os.makedirs(server_dir, exist_ok=True)

    # Prompt for specific server subchoices
    if server_type == "java":
        print("Choose a Java server type:")
        print("1. Vanilla Java")
        print("2. Spigot Java")
        subchoice = input("Enter your choice (1 or 2): ")
        if subchoice == "1":
            server_url = "https://dummy-vanilla-java-server-url.com/server.jar"
        elif subchoice == "2":
            server_url = "https://dummy-spigot-java-server-url.com/server.jar"
        else:
            print("Invalid choice.")
            exit(1)
    elif server_type == "bedrock":
        print("Choose a Bedrock server type:")
        print("1. Vanilla Bedrock")
        print("2. PocketMine Bedrock")
        subchoice = input("Enter your choice (1 or 2): ")
        if subchoice == "1":
            server_url = "https://dummy-vanilla-bedrock-server-url.com/server.exe"
        elif subchoice == "2":
            server_url = "https://dummy-pocketmine-bedrock-server-url.com/server.exe"
        else:
            print("Invalid choice.")
            exit(1)
    else:
        print("Invalid server type.")
        exit(1)

    # Download the server file based on the subchoice
    server_file = os.path.join(server_dir, "server_file")
    download_server(server_url, server_file)

    # Install additional dependencies or perform any other setup steps here

    print("Minecraft server installation completed.")

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
        print("Invalid choice.")
        exit(1)

    # Prompt for installation confirmation
    print(f"You have chosen to install a {server_type.capitalize()} server.")
    confirmation = input("Proceed with the installation? (y/n): ")

    if confirmation.lower() != "y":
        print("Installation cancelled.")
        exit(0)

    # Install the server
    install_server(server_type)

if __name__ == "__main__":
    main()
    # Prompt for specific server subchoices
    if server_type == "java":
        print("Choose a Java server type:")
        print("1. Vanilla Java")
        print("2. Spigot Java")
        subchoice = input("Enter your choice (1 or 2): ")
        if subchoice == "1":
            server_url = "https://dummy-vanilla-java-server-url.com/server.jar"
        elif subchoice == "2":
            server_url = "https://dummy-spigot-java-server-url.com/server.jar"
        else:
            print("Invalid choice.")
            exit(1)
    elif server_type == "bedrock":
        print("Choose a Bedrock server type:")
        print("1. Vanilla Bedrock")
        print("2. PocketMine Bedrock")
        subchoice = input("Enter your choice (1 or 2): ")
        if subchoice == "1":
            server_url = "https://dummy-vanilla-bedrock-server-url.com/server.exe"
        elif subchoice == "2":
            server_url = "https://dummy-pocketmine-bedrock-server-url.com/server.exe"
        else:
            print("Invalid choice.")
            exit(1)
    else:
        print("Invalid server type.")
        exit(1)

    # Download the server file based on the subchoice
    server_file = os.path.join(server_dir, "server_file")
    download_server(server_url, server_file)

    # Install additional dependencies or perform any other setup steps here

    print("Minecraft server installation completed.")

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
        print("Invalid choice.")
        exit(1)

    # Prompt for installation confirmation
    print(f"You have chosen to install a {server_type.capitalize()} server.")
    confirmation = input("Proceed with the installation? (y/n): ")

    if confirmation.lower() != "y":
        print("Installation cancelled.")
        exit(0)

    # Install the server
    install_server(server_type)

if __name__ == "__main__":
    main()
