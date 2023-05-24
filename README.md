# Minecraft Server Installer

This is a script to simplify the process of downloading and installing Minecraft servers on different platforms. It provides options for both Java Edition and Bedrock Edition servers.

## Features

- Download and install Minecraft servers with ease.
- Support for Java Edition and Bedrock Edition.
- User-generated server names for added customization.

## Prerequisites

- Windows:
  - Administrative privileges are recommended.
- Unix-like Systems (Linux, macOS, Termux):
  - Administrative privileges may be required for certain installation steps.

## Usage

1. Clone or download this repository to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.

### Windows

- Run `start-windows.cmd` to start the script on Windows systems.
- The script will prompt you to install Chocolatey (package manager) and Python if not already installed. It will install these prerequisites for you if you choose to proceed with the installation.
- Once Chocolatey and Python are installed, the script will proceed with downloading and installing the Minecraft server.

### Unix-like Systems (Linux, macOS, Termux)

- Run `start-unix.sh` to start the script on Unix-like systems.
- The script will check for Python installation using the package manager first. If Python is not found, it will prompt you to install it manually or provide the installation link. It will handle the installation for you if you choose to proceed with it.
- After verifying or installing Python, the script will proceed with downloading and installing the Minecraft server.

**Note**: Administrative privileges may be required for certain installation steps. Make sure to run the script as an administrator on Windows or provide necessary permissions on Unix-like systems.

## License

This project is licensed under the [MIT License](LICENSE).

