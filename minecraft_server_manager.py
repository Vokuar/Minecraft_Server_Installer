#!/usr/bin/env python3
"""
Minecraft Server Installer and Launcher
Supports both GUI and command-line interfaces
Works on Windows, macOS, Linux, and Termux
"""

import os
import sys
import platform
import subprocess
import time
import json
import requests
import shutil
import argparse
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Define constants
SERVER_MANAGER_DIR = os.path.join(os.path.expanduser("~"), ".minecraft_server_manager")
SERVER_DATA_FILE = os.path.join(SERVER_MANAGER_DIR, "servers.json")
CONFIG_FILE = os.path.join(SERVER_MANAGER_DIR, "config.json")
LOG_DIR = os.path.join(SERVER_MANAGER_DIR, "logs")
VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"

# Server URLs
SERVER_URLS = {
    "java": {
        "vanilla": lambda version: get_vanilla_url(version),
        "paper": lambda version: get_paper_url(version),
        "fabric": lambda version: f"https://maven.fabricmc.net/net/fabricmc/fabric-server-launcher/{get_fabric_version(version)}/fabric-server-launcher-{get_fabric_version(version)}-universal.jar",
        "forge": lambda version: f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{get_forge_build(version)}/forge-{version}-{get_forge_build(version)}-installer.jar"
    },
    "bedrock": {
        "vanilla": "https://minecraft.azureedge.net/bin-win/bedrock-server-1.20.15.01.zip",
        "pocketmine": "https://github.com/pmmp/PocketMine-MP/releases/latest/download/PocketMine-MP.phar",
        "nukkit": "https://ci.opencollab.dev/job/NukkitX/job/Nukkit/job/master/lastSuccessfulBuild/artifact/target/nukkit-1.0-SNAPSHOT.jar"
    }
}

# Ensure directories exist
os.makedirs(SERVER_MANAGER_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def is_termux():
    """Check if running in Termux environment"""
    return "com.termux" in os.getenv("PREFIX", "")

def is_gui_available():
    """Check if GUI is available"""
    if is_termux():
        return "DISPLAY" in os.environ or "WAYLAND_DISPLAY" in os.environ
    return True  # Assume GUI available on desktop systems

def hide_folder(path):
    """Hide the server directory."""
    if platform.system() == "Windows":
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(path, 2)  # FILE_ATTRIBUTE_HIDDEN
        except:
            return False
    elif platform.system() in ["Darwin", "Linux"]:
        try:
            # Add dot prefix to hide on Unix systems
            hidden_path = os.path.join(os.path.dirname(path), "." + os.path.basename(path))
            os.rename(path, hidden_path)
            return hidden_path
        except:
            return False
    return path

def get_available_versions(server_type="java"):
    """Get available Minecraft versions from Mojang API"""
    try:
        response = requests.get(VERSION_MANIFEST_URL)
        data = response.json()
        
        if server_type == "java":
            return [v['id'] for v in data['versions'] if v['type'] == 'release']
        else:  # Bedrock
            # Filter for Bedrock versions (simplified)
            return [v['id'] for v in data['versions'] if v['id'].startswith('1.') and '.' in v['id']]
    except:
        # Fallback versions
        return ["1.20.1", "1.19.4", "1.18.2", "1.17.1", "1.16.5"]

def get_paper_build(version):
    """Get latest Paper build number for a version"""
    url = f"https://api.papermc.io/v2/projects/paper/versions/{version}"
    try:
        response = requests.get(url)
        data = response.json()
        return data['builds'][-1]  # Latest build
    except:
        return None

def get_fabric_version(version):
    """Get compatible Fabric version"""
    # Simplified - in reality this would query Fabric API
    return "1.0.0"  # Placeholder

def get_forge_build(version):
    """Get latest Forge build for a version"""
    # Simplified - would query Forge files
    return "47.1.0"  # Placeholder

def get_vanilla_url(version):
    """Get Vanilla server URL for a specific version"""
    try:
        response = requests.get(VERSION_MANIFEST_URL)
        manifest = response.json()
        
        # Find version details
        version_entry = next(v for v in manifest['versions'] if v['id'] == version)
        version_manifest = requests.get(version_entry['url']).json()
        return version_manifest['downloads']['server']['url']
    except:
        # Fallback URL
        return f"https://piston-data.mojang.com/v1/objects/{version}/server.jar"

def get_paper_url(version):
    """Get Paper server URL"""
    build = get_paper_build(version)
    if not build:
        raise ValueError(f"No Paper build found for {version}")
    return f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar"

def get_server_data():
    """Load server data from JSON file"""
    if os.path.exists(SERVER_DATA_FILE):
        try:
            with open(SERVER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'servers': []}
    return {'servers': []}

def save_server_data(data):
    """Save server data to JSON file"""
    with open(SERVER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_server(server_name, version, server_type="vanilla", implementation="java"):
    """Create a new Minecraft server"""
    # Create server directory
    server_dir_name = f"minecraft_server_{server_name}"
    server_dir = os.path.join(os.path.expanduser("~"), server_dir_name)
    os.makedirs(server_dir, exist_ok=True)
    
    # Hide the folder
    server_dir = hide_folder(server_dir) or server_dir
    
    # Get server URL
    try:
        url = SERVER_URLS[implementation][server_type](version)
    except KeyError:
        raise ValueError(f"Unsupported server type: {implementation}/{server_type}")
    
    # Download server jar
    jar_path = os.path.join(server_dir, "server.jar")
    download_file(url, jar_path)
    
    # Create essential files
    eula_path = os.path.join(server_dir, "eula.txt")
    with open(eula_path, 'w') as f:
        f.write("eula=true\n")
    
    # Save to server data
    server_data = get_server_data()
    server_data['servers'].append({
        'name': server_name,
        'version': version,
        'type': server_type,
        'implementation': implementation,
        'path': server_dir,
        'created': time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_server_data(server_data)
    
    return server_dir

def download_file(url, file_path):
    """Download a file with progress and error handling"""
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"Downloading... {progress:.1f}%", end='\r')
            
            print("\nDownload complete.")
            return True
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return False

def start_server(server_directory):
    """Start an existing Minecraft server"""
    server_file = os.path.join(server_directory, "server.jar")
    log_file = os.path.join(LOG_DIR, f"{os.path.basename(server_directory)}.log")
    
    # Create log file if it doesn't exist
    open(log_file, 'a').close()
    
    # Start server
    if platform.system() == "Windows":
        subprocess.Popen(
            ["java", "-Xmx1024M", "-Xms1024M", "-jar", server_file, "nogui"],
            cwd=server_directory,
            stdout=open(log_file, 'a'),
            stderr=subprocess.STDOUT
        )
    else:
        # Use screen for Linux/macOS/Termux
        screen_name = f"mc_{os.path.basename(server_directory)}"
        cmd = f"screen -dmS {screen_name} java -Xmx1024M -Xms1024M -jar {server_file} nogui"
        subprocess.Popen(cmd, shell=True, cwd=server_directory)
    
    print(f"Server started in background. Log: {log_file}")

def stop_server(server_directory):
    """Stop an existing Minecraft server"""
    if platform.system() == "Windows":
        # Find and kill Java process
        subprocess.run(["taskkill", "/f", "/im", "java.exe"], stderr=subprocess.DEVNULL)
    else:
        # Stop screen session
        screen_name = f"mc_{os.path.basename(server_directory)}"
        subprocess.run(["screen", "-S", screen_name, "-X", "stuff", "stop\n"])
        subprocess.run(["screen", "-S", screen_name, "-X", "quit"])

def restart_server(server_directory):
    """Restart an existing Minecraft server"""
    stop_server(server_directory)
    time.sleep(5)  # Wait for server to stop
    start_server(server_directory)

def delete_server(server_directory):
    """Delete a server and its data"""
    # Remove from server data
    server_data = get_server_data()
    server_data['servers'] = [s for s in server_data['servers'] if s['path'] != server_directory]
    save_server_data(server_data)
    
    # Remove server directory
    try:
        shutil.rmtree(server_directory)
    except Exception as e:
        return f"Could not delete server directory: {e}"
    
    # Remove log file
    log_file = os.path.join(LOG_DIR, f"{os.path.basename(server_directory)}.log")
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
        except:
            pass
    
    return "Server deleted successfully"

def cli_install_server():
    """Command-line interface for server installation"""
    print("===== Minecraft Server Installer (CLI) =====")
    
    # Get server details
    server_name = input("Enter server name: ").strip()
    if not server_name:
        print("Server name cannot be empty")
        return
    
    print("Select implementation:")
    print("1. Java Edition")
    print("2. Bedrock Edition")
    impl_choice = input("Choice (1-2): ").strip()
    implementation = "java" if impl_choice == "1" else "bedrock"
    
    versions = get_available_versions(implementation)
    print(f"Available versions: {', '.join(versions[:5])}{'...' if len(versions) > 5 else ''}")
    version = input(f"Enter version [{versions[0]}]: ").strip() or versions[0]
    
    if implementation == "java":
        print("Select server type:")
        print("1. Vanilla")
        print("2. Paper")
        print("3. Fabric")
        print("4. Forge")
        type_choice = input("Choice (1-4): ").strip()
        types = ["vanilla", "paper", "fabric", "forge"]
        server_type = types[int(type_choice) - 1] if type_choice in "1234" else "vanilla"
    else:
        server_type = "vanilla"
    
    # Create server
    try:
        server_dir = create_server(server_name, version, server_type, implementation)
        print(f"Server created at: {server_dir}")
        
        # Start server to generate files
        print("Starting server to initialize files...")
        start_server(server_dir)
        time.sleep(30)
        stop_server(server_dir)
        print("Server initialized successfully")
    except Exception as e:
        print(f"Error creating server: {str(e)}")

def cli_manage_servers():
    """Command-line interface for server management"""
    server_data = get_server_data()
    if not server_data['servers']:
        print("No servers found")
        return
    
    print("===== Minecraft Server Manager (CLI) =====")
    print("ID | Name          | Version | Type")
    print("-" * 40)
    
    for i, server in enumerate(server_data['servers'], 1):
        print(f"{i:2} | {server['name'][:12]:12} | {server['version']:7} | {server['type']}")
    
    choice = input("\nSelect server ID (0 to exit): ").strip()
    if not choice.isdigit() or int(choice) == 0:
        return
    
    server_id = int(choice) - 1
    if server_id < 0 or server_id >= len(server_data['servers']):
        print("Invalid selection")
        return
    
    server = server_data['servers'][server_id]
    
    print("\nActions:")
    print("1. Start server")
    print("2. Stop server")
    print("3. Restart server")
    print("4. Delete server")
    action = input("Choice (1-4): ").strip()
    
    if action == "1":
        start_server(server['path'])
    elif action == "2":
        stop_server(server['path'])
    elif action == "3":
        restart_server(server['path'])
    elif action == "4":
        result = delete_server(server['path'])
        print(result)

def gui_install_server():
    """GUI interface for server installation"""
    class InstallerGUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Minecraft Server Installer")
            self.geometry("500x400")
            self.resizable(False, False)
            
            # Variables
            self.server_name = tk.StringVar()
            self.version = tk.StringVar()
            self.server_type = tk.StringVar(value="vanilla")
            self.implementation = tk.StringVar(value="java")
            self.versions = []
            
            self.create_widgets()
            self.load_versions()
            
        def create_widgets(self):
            ttk.Label(self, text="Server Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            ttk.Entry(self, textvariable=self.server_name, width=30).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            ttk.Label(self, text="Implementation:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
            impl_frame = ttk.Frame(self)
            impl_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
            ttk.Radiobutton(impl_frame, text="Java", variable=self.implementation, value="java", command=self.load_versions).pack(side="left")
            ttk.Radiobutton(impl_frame, text="Bedrock", variable=self.implementation, value="bedrock", command=self.load_versions).pack(side="left", padx=10)
            
            ttk.Label(self, text="Version:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
            self.version_combo = ttk.Combobox(self, textvariable=self.version, width=15)
            self.version_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
            
            ttk.Label(self, text="Server Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
            self.type_combo = ttk.Combobox(self, textvariable=self.server_type, width=15)
            self.type_combo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
            
            ttk.Button(self, text="Install Server", command=self.install).grid(row=4, column=0, columnspan=2, pady=20)
            
            self.status = ttk.Label(self, text="", foreground="blue")
            self.status.grid(row=5, column=0, columnspan=2)
            
        def load_versions(self):
            self.versions = get_available_versions(self.implementation.get())
            self.version_combo['values'] = self.versions
            if self.versions:
                self.version.set(self.versions[0])
            
            # Update server types
            if self.implementation.get() == "java":
                self.type_combo['values'] = ["vanilla", "paper", "fabric", "forge"]
                self.server_type.set("vanilla")
            else:
                self.type_combo['values'] = ["vanilla", "pocketmine", "nukkit"]
                self.server_type.set("vanilla")
        
        def install(self):
            server_name = self.server_name.get().strip()
            if not server_name:
                self.status.config(text="Server name cannot be empty", foreground="red")
                return
                
            version = self.version.get()
            server_type = self.server_type.get()
            implementation = self.implementation.get()
            
            try:
                self.status.config(text="Creating server...", foreground="blue")
                self.update()
                
                server_dir = create_server(server_name, version, server_type, implementation)
                
                self.status.config(text="Starting server for initialization...", foreground="blue")
                self.update()
                
                start_server(server_dir)
                self.after(30000, self.finalize_installation, server_dir)  # Wait 30 seconds
                
            except Exception as e:
                self.status.config(text=f"Error: {str(e)}", foreground="red")
        
        def finalize_installation(self, server_dir):
            stop_server(server_dir)
            self.status.config(text=f"Server installed at: {server_dir}", foreground="green")
    
    app = InstallerGUI()
    app.mainloop()

def gui_manage_servers():
    """GUI for server management"""
    class ServerManagerGUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Minecraft Server Manager")
            self.geometry("800x600")
            self.minsize(600, 400)
            
            self.servers = []
            self.selected_server = None
            
            self.create_widgets()
            self.load_servers()
            
        def create_widgets(self):
            # Server list
            self.tree = ttk.Treeview(self, columns=("name", "version", "type"), show="headings")
            self.tree.heading("name", text="Server Name")
            self.tree.heading("version", text="Version")
            self.tree.heading("type", text="Type")
            self.tree.column("name", width=200)
            self.tree.column("version", width=100)
            self.tree.column("type", width=100)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)
            self.tree.bind("<<TreeviewSelect>>", self.on_select)
            
            # Action buttons
            btn_frame = ttk.Frame(self)
            btn_frame.pack(fill="x", padx=10, pady=10)
            
            self.start_btn = ttk.Button(btn_frame, text="Start", command=self.start_server, state="disabled")
            self.start_btn.pack(side="left", padx=5)
            
            self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_server, state="disabled")
            self.stop_btn.pack(side="left", padx=5)
            
            self.restart_btn = ttk.Button(btn_frame, text="Restart", command=self.restart_server, state="disabled")
            self.restart_btn.pack(side="left", padx=5)
            
            self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_server, state="disabled")
            self.delete_btn.pack(side="left", padx=5)
            
            # Status bar
            self.status = ttk.Label(self, text="Ready", relief="sunken", anchor="w")
            self.status.pack(side="bottom", fill="x")
            
        def load_servers(self):
            self.tree.delete(*self.tree.get_children())
            server_data = get_server_data()
            self.servers = server_data.get('servers', [])
            
            for server in self.servers:
                self.tree.insert("", "end", values=(
                    server['name'],
                    server['version'],
                    server['type']
                ), tags=(server['path'],))
            
            self.status.config(text=f"Loaded {len(self.servers)} servers")
        
        def on_select(self, event):
            selection = self.tree.selection()
            if selection:
                self.selected_server = self.tree.item(selection[0], "tags")[0]
                self.start_btn.config(state="normal")
                self.stop_btn.config(state="normal")
                self.restart_btn.config(state="normal")
                self.delete_btn.config(state="normal")
            else:
                self.selected_server = None
                self.start_btn.config(state="disabled")
                self.stop_btn.config(state="disabled")
                self.restart_btn.config(state="disabled")
                self.delete_btn.config(state="disabled")
        
        def start_server(self):
            if self.selected_server:
                self.status.config(text="Starting server...")
                self.update()
                start_server(self.selected_server)
                self.status.config(text="Server started in background")
        
        def stop_server(self):
            if self.selected_server:
                self.status.config(text="Stopping server...")
                self.update()
                stop_server(self.selected_server)
                self.status.config(text="Server stopped")
        
        def restart_server(self):
            if self.selected_server:
                self.status.config(text="Restarting server...")
                self.update()
                restart_server(self.selected_server)
                self.status.config(text="Server restarted")
        
        def delete_server(self):
            if self.selected_server:
                if messagebox.askyesno("Confirm Delete", "Delete this server and all its files?"):
                    result = delete_server(self.selected_server)
                    self.status.config(text=result)
                    self.load_servers()
    
    app = ServerManagerGUI()
    app.mainloop()

def main():
    """Main entry point with mode selection"""
    parser = argparse.ArgumentParser(description="Minecraft Server Installer and Manager")
    parser.add_argument("--cli", action="store_true", help="Force command-line interface")
    parser.add_argument("--gui", action="store_true", help="Force graphical interface")
    parser.add_argument("--install", action="store_true", help="Run installer")
    parser.add_argument("--manage", action="store_true", help="Run server manager")
    args = parser.parse_args()
    
    # Determine interface mode
    if args.cli:
        use_gui = False
    elif args.gui:
        use_gui = True
    else:
        use_gui = is_gui_available() and not is_termux()
    
    # Determine operation
    if args.install:
        operation = "install"
    elif args.manage:
        operation = "manage"
    else:
        # Ask user what they want to do
        if use_gui:
            root = tk.Tk()
            root.withdraw()
            choice = messagebox.askquestion("Minecraft Tools", "What would you like to do?", 
                                          detail="Install a new server or manage existing servers?",
                                          icon="question", type="yesnocancel",
                                          default="yes")
            if choice == "yes":
                operation = "install"
            elif choice == "no":
                operation = "manage"
            else:
                return
        else:
            print("1. Install new server")
            print("2. Manage existing servers")
            choice = input("Choice (1-2): ").strip()
            operation = "install" if choice == "1" else "manage"
    
    # Execute operation
    if operation == "install":
        if use_gui:
            gui_install_server()
        else:
            cli_install_server()
    else:  # manage
        if use_gui:
            gui_manage_servers()
        else:
            cli_manage_servers()

if __name__ == "__main__":
    main()
