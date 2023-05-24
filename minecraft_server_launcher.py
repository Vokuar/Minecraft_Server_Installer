import os
import subprocess
import platform
import tkinter as tk
import tkinter.ttk as ttk

# Define constants
SERVER_MANAGER_DIR = os.path.join(os.path.expanduser("~"), ".minecraft_server_manager")


def hide_folder(path):
    """Hide the server directory."""
    if platform.system() == "Windows":
        try:
            import win32file
            win32file.SetFileAttributes(path, win32file.FILE_ATTRIBUTE_HIDDEN)
        except ImportError:
            print("Unable to hide folder on Windows. Please hide the folder manually.")
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        try:
            subprocess.run(["chflags", "hidden", path])
        except subprocess.CalledProcessError:
            print("Unable to hide folder on macOS or Linux. Please hide the folder manually.")


def get_server_directories():
    """Scan the home directory for server directories."""
    server_directories = []
    for item in os.listdir(os.path.expanduser("~")):
        item_path = os.path.join(os.path.expanduser("~"), item)
        if os.path.isdir(item_path) and os.path.basename(item_path).startswith(".minecraft_server_"):
            server_directories.append(item_path)
    return server_directories


def start_server(server_directory):
    """Start an existing Minecraft server."""
    server_file = os.path.join(server_directory, "server.jar")
    subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", server_file, "nogui"], cwd=server_directory)


def stop_server(server_directory):
    """Stop an existing Minecraft server."""
    screen_sessions = subprocess.check_output(["screen", "-list"], universal_newlines=True)
    for line in screen_sessions.split('\n'):
        if server_directory in line:
            session_name = line.split('\t')[0].strip()
            subprocess.run(["screen", "-S", session_name, "-X", "stuff", "stop\n"])
            subprocess.run(["screen", "-S", session_name, "-X", "quit"])


def restart_server(server_directory):
    """Restart an existing Minecraft server."""
    stop_server(server_directory)
    start_server(server_directory)


class ServerManager:
    def __init__(self, root):
        self.servers = []
        self.server_box = None
        self.start_button = None
        self.stop_button = None
        self.restart_button = None

        self.root = root
        self.root.title("Minecraft Server Manager")
        self.root.resizable(width=False, height=False)

        self._setup_ui()
        self._update_server_list()

    def _setup_ui(self):
        # Server box
        servers_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        servers_frame.pack(side="left", fill="y")

        server_label = ttk.Label(servers_frame, text="Servers")
        server_label.pack(side="top")

        self.server_box = tk.Listbox(servers_frame, width=25, height=15)
        self.server_box.pack(side="top")

        scrollbar = ttk.Scrollbar(servers_frame, orient="vertical", command=self.server_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.server_box.config(yscrollcommand=scrollbar.set)

        # Button frame
        button_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        button_frame.pack(side="right", fill="y")

        self.start_button = ttk.Button(button_frame, text="Start", state=tk.DISABLED, command=self._start_server)
        self.start_button.pack(side="top", fill="x")
        self.stop_button = ttk.Button(button_frame, text="Stop", state=tk.DISABLED, command=self._stop_server)
        self.stop_button.pack(side="top", fill="x")
        self.restart_button = ttk.Button(button_frame, text="Restart", state=tk.DISABLED, command=self._restart_server)
        self.restart_button.pack(side="top", fill="x")

        # Refresh button
        refresh_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        refresh_frame.pack(side="bottom", fill="x")

        refresh_button = ttk.Button(refresh_frame, text="Refresh", command=self._update_server_list)
        refresh_button.pack(fill="x")

        # Bindings
        self.server_box.bind("<Double-Button-1>", self._start_server)

    def _update_server_list(self, event=None):
        # Clear the server list
        self.server_box.delete(0, tk.END)
        self.servers = []

        # Get the list of server directories
        server_directories = get_server_directories()

        # Add each server directory to the list box
        for dir_path in server_directories:
            self.servers.append(dir_path)
            dir_name = os.path.basename(dir_path).replace(".minecraft_server_", "")
            self.server_box.insert(tk.END, dir_name)

        # Select the first server in the list
        if self.servers:
            self.server_box.selection_set(0)
            self.server_box.event_generate("<<ListboxSelect>>")

    def _start_server(self, event=None):
        # Get the selected server directory
        selected_index = self.server_box.curselection()
        if selected_index:
            selected_server = self.servers[selected_index[0]]
            self.start_button["state"] = tk.DISABLED
            self.stop_button["state"] = tk.NORMAL
            self.restart_button["state"] = tk.NORMAL
            start_server(selected_server)

    def _stop_server(self, event=None):
        # Get the selected server directory
        selected_index = self.server_box.curselection()
        if selected_index:
            selected_server = self.servers[selected_index[0]]
            self.start_button["state"] = tk.NORMAL
            self.stop_button["state"] = tk.DISABLED
            self.restart_button["state"] = tk.DISABLED
            stop_server(selected_server)

    def _restart_server(self, event=None):
        # Get the selected server directory
        selected_index = self.server_box.curselection()
        if selected_index:
            selected_server = self.servers[selected_index[0]]
            self.start_button["state"] = tk.DISABLED
            self.stop_button["state"] = tk.NORMAL
            self.restart_button["state"] = tk.DISABLED
            restart_server(selected_server)


if __name__ == "__main__":
    # Create the server manager directory if it doesn't exist
    os.makedirs(SERVER_MANAGER_DIR, exist_ok=True)

    # Create the GUI
    root = tk.Tk()
    server_manager = ServerManager(root)
    root.mainloop()

