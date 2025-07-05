# Minecraft Server Installer & Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Platforms: Windows, Linux, macOS, Termux](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Termux-blue)

A cross-platform tool to easily install and manage Minecraft servers with both GUI and command-line interfaces. Supports Java Edition (Vanilla, Paper, Fabric, Forge) and Bedrock Edition (Vanilla, PocketMine, Nukkit).

## Features ✨

- **One-Click Installation**: Set up Minecraft servers in seconds
- **Multi-Platform Support**: Works on Windows, macOS, Linux, and Android (Termux)
- **Dual Interface**: Choose between graphical (GUI) or command-line (CLI) interface
- **Server Types Supported**:
  - Java Edition: Vanilla, Paper, Fabric, Forge
  - Bedrock Edition: Vanilla, PocketMine, Nukkit
- **Automatic Updates**: Fetches latest server versions from official sources
- **Server Management**: Start, stop, restart, and delete servers
- **Unified Experience**: Consistent workflow across all platforms
- **Lightweight**: Minimal dependencies, self-contained design

## Installation ⚙️

### Windows
```cmd
curl -O https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main/install-windows.cmd
install-windows.cmd
```

### Linux/macOS
```bash
curl -O https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main/install-unix.sh
chmod +x install-unix.sh
./install-unix.sh
```

### Termux (Android)
```bash
curl -O https://raw.githubusercontent.com/Vokuar/Minecraft_Server_Installer/main/install-termux.sh
bash install-termux.sh
```

## Usage 🚀

### Graphical Interface (Desktop)

1. Run the installer script
2. Choose between:
   - **Install New Server**: Create a new Minecraft server
   - **Manage Servers**: Control existing servers

### Command-Line Interface (Termux/Advanced)
```bash
# Install a new server
python Minecraft_server_installer.py --install --cli

# Manage existing servers
python Minecraft_server_installer.py --manage --cli
```

#### CLI Examples:
```bash
# Create a Java Vanilla 1.20.1 server
> python Minecraft_server_installer.py --install --cli
Server name: MyVanillaServer
Implementation (java/bedrock): java
Version [1.20.1]: 
Server type (vanilla/paper/fabric/forge): vanilla

# Start a server
> python Minecraft_server_installer.py --manage --cli
1. MyVanillaServer (1.20.1, vanilla)
2. MyPaperServer (1.20.1, paper)
Select server: 1
Action (start/stop/restart/delete): start
```

## System Requirements ℹ️

- **Windows**: Windows 10 or newer
- **Linux**: Most modern distributions
- **macOS**: 10.15 Catalina or newer
- **Termux**: Latest version from F-Droid
- **Memory**: At least 2GB RAM (4GB recommended for servers)
- **Storage**: 500MB free space per server

## Advanced Options ⚒️

| Flag               | Description                          |
|--------------------|--------------------------------------|
| `--cli`            | Force command-line interface         |
| `--gui`            | Force graphical interface            |
| `--install`        | Run server installer                 |
| `--manage`         | Run server manager                   |
| `--version`        | Show version information             |
| `--help`           | Show help message                    |

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support or feature requests, please [open an issue](https://github.com/Vokuar/Minecraft_Server_Installer/issues).
