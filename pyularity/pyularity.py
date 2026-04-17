# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, exists, expanduser
from os import name
import time
import subprocess
import threading
from sys import argv
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
import zmq

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pycurity.pyhash import text_hashing_function

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyularity.yaml")


class Pyularity(object):
    """"""

    HOST = "127.0.0.1"
    PORT = 65432
    PYTHON = "python"
    PYTHON_VERSION = "3.12"

    def __init__(self, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("Pyularity").override(cfg)
        self.app_name = self.config.dikt.get("app_name", None)
        self.concurrent_limit = self.config.dikt.get("concurrent_limit", 5)
        self.app_path = None
        self.venv_path = None
        self.is_installed = False
        self.main_app = None
        self.manifest = {}
        self.new_modules = []
        self.new_instances = []
        self.package = None
        self.processes = {}
        self.python_executable = None
        self.scripts = None
        self.socket = None
        self.startup_app = None
        self.running = False
        self.version = None

    def add_process(self, process):
        """"""
        self.processes[process.pid] = process
        return self

    def check_installed(self):
        """"""
        return True

    def check_process(self, pid):
        """
        Checks if a process is still running.

        :param pid: Process ID to check.
        :return: Boolean indicating whether the process is running.
        """
        self.failed_processes = []
        if pid in self.processes:
            process = self.processes[pid]
            status = process.poll()
            if status is None:
                logma.info(f"Process {pid} is running.")
                return True
            else:
                self.failed_processes.append(pid)
                logma.info(f"Process {pid} has stopped with exit code {status}.")
                return False
        else:
            logma.info(f"Process with PID {pid} not found.")
            return False
        return self

    def check_update(self):
        """"""
        return self

    def close(self):
        """"""
        self.stop_all_processes()
        return self

    def close_instance(self, instance_id):
        """"""
        self.stop_process(instance_id)
        if len(self.processes) == 0:
            self.stop_server()
        return self

    def compare_manifest(self, manifest):
        """"""
        self.new_modules = []
        for module in manifest:
            if module not in self.manifest:
                self.new_modules.append(module)
        return True

    def connect(self):
        """"""
        context = zmq.Context()  # Create a ZeroMQ context
        self.socket = context.socket(zmq.REP)  # Create a REP (Reply) socket
        self.socket.bind(f"{self.HOST}:{self.PORT}")  # Bind to a TCP address
        return self

    def get_hash(self, application_NCD):
        """"""
        _hash = ""  # connect to some blockchain service
        return _hash

    def get_manifest(self):
        """"""
        manifest = ""
        self.compare_manifest(manifest)
        if manifest != self.manifest:
            self.manifest = manifest
        return self.manifest

    def initialize_communications_server(self):
        """"""
        self.comserv = threading.Thread(target=self._start_server, daemon=True)
        self.comserv.start()
        self.running = True
        return self

    def install_failed(self):
        """"""
        return self

    def install_pip(self, location):
        """"""
        cmd = [self.python_executable, "-m", "pip", "install", location, "--upgrade"]
        # if location.startswith("http"):
        #     cmd = [self.python_executable, "-m", "pip", "install", location, "--upgrade"]
        # elif location.startswith("file"):
        #     cmd = [self.python_executable, "-m", "pip", "install", location, "--upgrade"]  # , "--no-deps"]
        # else:
        #     cmd = [self.python_executable, "-m", "pip", "install", location, "--upgrade"]
        self.run_cmd(cmd)

    def launch_app(self):
        """"""
        initialize = True
        loop = 0
        while True:
            logma.info("Launch Instance")
            self.set_virtual_environment()
            cnt = 0
            while not self.check_installed():  # checking for python modules installed
                if cnt > 3:
                    self.install_failed()
                    break
                while True:
                    process_id = self.start_process("install")
                    if not self.check_process(process_id):
                        break
                cnt += 1
            if self.check_update():
                self.run_update()
            if initialize:
                self.initialize_communications_server()
                self.launch_instance()
                initialize = False
            # check comms
            if self.check_comms():
                for instance in self.new_instances:
                    self.launch_instance(instance)
            # check processes
            for process in self.processes:
                if self.check_process(process):
                    continue
                else:
                    logma.info(f"Process {process} has stopped. Restarting Instance.")
            for pid in self.failed_processes:
                self.stop_process(pid)
            self.failed_processes = []
            time.sleep(10)
            loop += 1
            if len(self.processes) == 0:
                break
        return self

    def launch_instance(self, instance_id=None, *args, **kwargs):
        """"""
        if instance_id is None:
            instance_id = None
        if len(self.processes) > self.concurrent_limit:
            message = f"This Program is limited to {self.concurrent_limit} concurrent instances."
            message += f"Please close an instance to launch another."
            self.main_app.dialog.show(message)
            return None
        script = f"python -m {self.app_name}"
        self.start_process(script, instance_id)
        return self

    def run(self):
        """"""
        self.set_paths()
        self.launch_app()

    def run_cmd(self, cmd):
        """"""
        logma.info(f"Running Command: {cmd}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.add_process(process)
        logma.info(f"Started process with PID: {process.pid}")
        return process.pid

    def run_update(self):
        """"""
        self.set_virtual_environment()
        self._update_modules()
        return self

    def set_main_app(self, app):
        """"""
        self.main_app = app
        return self

    def set_paths(self):
        """"""
        self.app_path = join(expanduser("~"), ".local", "share", self.app_name)
        self.venv_path = join(self.app_path, ".venv")
        return self

    def set_startup_app(self, app):
        """"""
        self.startup_app = app
        return self

    def set_virtual_environment(self, name="linux"):
        """"""
        if not exists(self.venv_path):
            raise Exception("Python Not Properly Installed for Pyularity based Application")
        if name == "linux":
            self.python_executable = join(self.venv_path, "bin", f"{self.PYTHON}{self.PYTHON_VERSION}")
        elif name == "macos":
            self.python_executable = join(self.venv_path, "bin", self.PYTHON)
        elif name == "windows":
            self.python_executable = join(self.venv_path, "Scripts", f"{self.PYTHON}.exe")
        else:
            raise Exception(f"Unknown OS Type: {name} not yet implemented.")
        return self

    def start_process(self, script_path, instance_id=None, *args, **kwargs):
        """
        Starts a Python script as a separate process.

        :param script_path: Path to the Python script to run.
        :param args: Additional arguments for the script.
        :return: Process ID.
        """
        if instance_id is not None:
            args = [instance_id] + list(args)
        cmd = [self.python_executable, script_path, *args]
        # try:
        logma.info(f"Starting process: {cmd}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.add_process(process)
        logma.info(f"Started process with PID: {process.pid}")
        return process.pid
        # except Exception as e:
        #     logma.info(f"Error starting process: {e}")
        #     return None
        # return self

    def stop_process(self, pid):
        """
        Stops a process by sending a SIGTERM signal.

        :param pid: Process ID to stop.
        """
        if pid in self.processes:
            process = self.processes[pid]
            stdout, stderr = process.communicate()
            # send these to a written file somewhere
            logma.info(f"Process stdout: {stdout}")
            logma.info(f"Process stderr: {stderr}")
            process.terminate()  # Send SIGTERM
            process.wait()  # Wait for the process to terminate
            logma.info(f"Terminated process with PID: {pid}")
            del self.processes[pid]
        else:
            logma.info(f"Process with PID {pid} not found.")
        return self

    def stop_all_processes(self):
        """
        Stops all managed processes.
        """
        logma.info("Stopping all processes...")
        for pid in list(self.processes.keys()):
            self.stop_process(pid)
        return self

    def stop_server(self):
        """Shuts down the callback server and all child processes."""
        self.running = False
        if hasattr(self, "server_socket"):
            self.server_socket.close()
        logma.info("Callback server and all processes have been stopped.")
        return self

    def _copy_to_install(self):
        """"""
        return self

    def _download(self):
        """"""
        self.manifest = self.get_manifest()
        self._copy_to_install()
        self._hash = text_hashing_function(self.manifest)
        return self

    def _install_modules(self):
        """"""
        for module in self.manifest:
            self.pip_install(module)
        return self

    def _start_server(self, *args, **kwargs):
        """"""
        self.connect()
        while True:
            # Wait for the next request from the client
            message = self.socket.recv_string()  # Receive UTF-8 string
            if message.split(":")[0] == "NEWINSTANCE":
                self.launch_instance(message.split(":")[1])
                self.socket.send_string("TRUE")  # Send UTF-8 string
            elif message.split(":")[0] == "CLOSEINSTANCE":
                self.close_instance(message.split(":")[1])
                self.socket.send_string("TRUE")
            elif message.split(":")[0] == "EXIT":
                self.close_instance(message.split(":")[1])
                break
            time.sleep(10)
        return self

    def _update_modules(self):
        """"""
        cmd = [self.python_executable, "-m", "pip", "install", "--upgrade", self.app_name]
        self.run_cmd(cmd)
        return self

    def _verify(self):
        """"""
        _hash = self.get_hash(self.application_NCD)
        if _hash != self._hash:
            return False
        return True


def main():
    """"""
    cfg = {}
    disk = Pyularity(cfg)
    disk.launch_app()


if __name__ == "__main__":
    start = dt.datetime.now()
    logma.info("Start")
    main()
    end = dt.datetime.now()
    logma.info(f"End Duration {end - start}")
# ====================================================================================================================||

#
# #!/usr/bin/env python3
# import os
# import subprocess
# import sys
# import platform
# import tempfile
# import urllib.request
# from pathlib import Path
# import argparse
#
# # Configuration
# VENV_DIR = ".venv"  # Virtual environment directory
# PYTHON_VERSION = "3.11"  # Desired Python version
# UV_VERSION = "0.4.25"  # uv version for standalone binary
# APP_NAME = "PySide6Example"  # Name for the application and icon
# ICON_NAME = "app_icon.png"  # Icon file (downloaded or provided)
# REQUIREMENTS = [
#     "PySide6>=6.5.0",  # PySide6 for GUI
#     "pyshortcuts>=1.9.0",  # For Windows/Linux shortcuts
#     "pyobjc-framework-Cocoa>=10.0; platform_system=='Darwin'",  # For macOS .app (conditional)
# ]
#
# def run_command(command, check=True, shell=True):
#     """Run a shell command and handle errors."""
#     try:
#         result = subprocess.run(command, shell=shell, check=check, text=True, capture_output=True)
#         return result
#     except subprocess.CalledProcessError as e:
#         print(f"Error running command: {command}")
#         print(f"Output: {e.stderr}")
#         sys.exit(1)
#     except FileNotFoundError:
#         print(f"Command not found: {command}")
#         sys.exit(1)
#
# def download_icon():
#     """Download a sample icon if not present."""
#     icon_path = Path(ICON_NAME)
#     if not icon_path.exists():
#         print(f"Downloading sample icon to {ICON_NAME}...")
#         sample_icon_url = "https://raw.githubusercontent.com/python/cpython/main/Doc/_static/py.png"  # Sample Python logo
#         try:
#             urllib.request.urlretrieve(sample_icon_url, icon_path)
#         except Exception as e:
#             print(f"Failed to download icon: {e}. Proceeding without custom icon.")
#             return None
#     return icon_path
#
# def create_desktop_icon():
#     """Create a platform-specific desktop icon to launch the application."""
#     print("Creating desktop icon...")
#     system = platform.system().lower()
#     script_path = Path(__file__).resolve()
#     python_bin = Path(VENV_DIR) / ("Scripts" if system == "windows" else "bin") / ("python.exe" if system == "windows" else "python")
#     icon_path = download_icon()
#
#     if system == "linux":
#         # Create .desktop file for Linux
#         desktop_dir = Path.home() / ".local" / "share" / "applications"
#         desktop_dir.mkdir(parents=True, exist_ok=True)
#         desktop_file = desktop_dir / f"{APP_NAME}.desktop"
#         icon_dest = icon_path or ""  # Use empty string if no icon
#         with open(desktop_file, "w") as f:
#             f.write(
#                 f"""[Desktop Entry]
# Name={APP_NAME}
# Exec={python_bin} {script_path}
# Type=Application
# Terminal=false
# Icon={icon_dest}
# Comment=PySide6 Example Application
# """
#             )
#         os.chmod(desktop_file, 0o755)
#         print(f"Created Linux desktop icon: {desktop_file}")
#
#     elif system == "windows":
#         # Create Windows shortcut using pyshortcuts
#         try:
#             from pyshortcuts import make_shortcut
#         except ImportError:
#             print("Error: pyshortcuts not installed. Skipping icon creation.")
#             return
#
#         desktop_dir = Path.home() / "Desktop"
#         shortcut_path = desktop_dir / f"{APP_NAME}.lnk"
#         make_shortcut(
#             script=str(script_path),
#             name=APP_NAME,
#             description="PySide6 Example Application",
#             executable=str(python_bin),
#             icon=str(icon_path) if icon_path else None,
#             folder=str(desktop_dir),
#         )
#         print(f"Created Windows shortcut: {shortcut_path}")
#
#     elif system == "darwin":
#         # Create macOS .app bundle or alias
#         try:
#             from Foundation import NSBundle
#             from Cocoa import NSWorkspace, NSImage
#         except ImportError:
#             print("Error: pyobjc-framework-Cocoa not installed. Creating simple alias instead.")
#
#             # Fallback: Create alias using osascript
#             alias_path = Path.home() / "Desktop" / f"{APP_NAME}.command"
#             with open(alias_path, "w") as f:
#                 f.write(
#                     f"""#!/bin/bash
# {python_bin} {script_path}
# """
#                 )
#             os.chmod(alias_path, 0o755)
#             print(f"Created macOS alias: {alias_path}")
#             return
#
#         # Create .app bundle (simplified)
#         app_dir = Path.home() / "Applications" / f"{APP_NAME}.app"
#         contents_dir = app_dir / "Contents"
#         macos_dir = contents_dir / "MacOS"
#         resources_dir = contents_dir / "Resources"
#         for d in (app_dir, contents_dir, macos_dir, resources_dir):
#             d.mkdir(parents=True, exist_ok=True)
#
#         # Copy icon
#         if icon_path:
#             icon_dest = resources_dir / icon_path.name
#             icon_dest.write_bytes(icon_path.read_bytes())
#
#         # Create executable script
#         exec_script = macos_dir / APP_NAME
#         with open(exec_script, "w") as f:
#             f.write(
#                 f"""#!/bin/bash
# {python_bin} {script_path}
# """
#             )
#         os.chmod(exec_script, 0o755)
#
#         # Create Info.plist
#         with open(contents_dir / "Info.plist", "w") as f:
#             f.write(
#                 f"""<?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
# <plist version="1.0">
# <dict>
#     <key>CFBundleExecutable</key>
#     <string>{APP_NAME}</string>
#     <key>CFBundleIconFile</key>
#     <string>{icon_path.name if icon_path else ''}</string>
#     <key>CFBundleName</key>
#     <string>{APP_NAME}</string>
#     <key>CFBundlePackageType</key>
#     <string>APPL</string>
# </dict>
# </plist>
# """
#             )
#         print(f"Created macOS .app bundle: {app_dir}")
#
# def install_uv():
#     """Install uv if not present, using platform-specific methods."""
#     print("Checking for uv...")
#     if run_command("uv --version", check=False).returncode == 0:
#         print("uv is already installed.")
#         return
#
#     print("Installing uv...")
#     system = platform.system().lower()
#     temp_dir = Path(tempfile.gettempdir())
#     uv_binary = temp_dir / ("uv.exe" if system == "windows" else "uv")
#
#     # Platform-specific uv installation
#     if system == "linux" or system == "darwin":
#         arch = "x86_64" if platform.machine() == "x86_64" else "arm64"
#         uv_url = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-{arch}-{'linux' if system == 'linux' else 'apple-darwin'}.tar.gz"
#         tar_file = temp_dir / "uv.tar.gz"
#         try:
#             print(f"Downloading uv from {uv_url}...")
#             urllib.request.urlretrieve(uv_url, tar_file)
#             run_command(f"tar -xzf {tar_file} -C {temp_dir}")
#             os.chmod(uv_binary, 0o755)
#         except Exception as e:
#             print(f"Failed to download uv: {e}")
#             print("Trying to install via pip...")
#             run_command("pip install uv")
#     elif system == "windows":
#         uv_url = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-x86_64-pc-windows-msvc.zip"
#         zip_file = temp_dir / "uv.zip"
#         try:
#             print(f"Downloading uv from {uv_url}...")
#             urllib.request.urlretrieve(uv_url, zip_file)
#             run_command(f"powershell -Command Expand-Archive -Path {zip_file} -DestinationPath {temp_dir}")
#         except Exception as e:
#             print(f"Failed to download uv: {e}")
#             print("Trying to install via pip...")
#             run_command("pip install uv")
#     else:
#         print(f"Unsupported platform: {system}")
#         sys.exit(1)
#
#     if uv_binary.exists():
#         os.environ["PATH"] = f"{temp_dir}{os.pathsep}{os.environ.get('PATH', '')}"
#         run_command(f"{uv_binary} --version")
#     else:
#         print("uv installation failed.")
#         sys.exit(1)
#
# def setup_environment():
#     """Set up virtual environment and install dependencies using uv."""
#     print("Setting up virtual environment...")
#     install_uv()
#     print(f"Creating virtual environment with Python {PYTHON_VERSION}...")
#     run_command(f"uv venv --python {PYTHON_VERSION} {VENV_DIR}")
#
#     if platform.system() == "Windows":
#         python_bin = Path(VENV_DIR) / "Scripts" / "python.exe"
#         uv_bin = Path(VENV_DIR) / "Scripts" / "uv.exe"
#     else:
#         python_bin = Path(VENV_DIR) / "bin" / "python"
#         uv_bin = Path(VENV_DIR) / "bin" / "uv"
#
#     if not python_bin.exists():
#         print(f"Error: Python not found in virtual environment at {python_bin}")
#         sys.exit(1)
#
#     print("Installing dependencies...")
#     requirements_str = " ".join(REQUIREMENTS)
#     run_command(f"{uv_bin} pip install {requirements_str}")
#
#     # Create desktop icon after setup
#     create_desktop_icon()
#
#     print("Setup complete!")
#
# def is_venv_active():
#     """Check if running inside the virtual environment."""
#     return sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
#
# def run_application():
#     """Run the PySide6 application."""
#     try:
#         from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
#         from PySide6.QtCore import Qt
#     except ImportError:
#         print("Error: PySide6 not installed. Ensure setup completed successfully.")
#         sys.exit(1)
#
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("PySide6 Example")
#     window.setFixedSize(400, 300)
#
#     central_widget = QWidget()
#     window.setCentralWidget(central_widget)
#     layout = QVBoxLayout(central_widget)
#
#     label = QLabel("Hello, PySide6!\nThis is a sample application.", alignment=Qt.AlignCenter)
#     layout.addWidget(label)
#
#     window.show()
#     sys.exit(app.exec())
#
# def main():
#     """Main function to handle setup or run."""
#     parser = argparse.ArgumentParser(description="Setup and run a PySide6 application.")
#     parser.add_argument("--setup", action="store_true", help="Run setup to create virtual environment and install dependencies")
#     args = parser.parse_args()
#
#     if args.setup or not is_venv_active():
#         setup_environment()
#         python_bin = Path(VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "python"
#         run_command(f"{python_bin} {__file__}", check=False)
#     else:
#         run_application()
#
# if __name__ == "__main__":
#     main()

# #!/usr/bin/env python3
# import os
# import subprocess
# import sys
# import platform
# import tempfile
# import urllib.request
# from pathlib import Path
# import argparse
#
# # Configuration
# VENV_DIR = ".venv"  # Virtual environment directory
# PYTHON_VERSION = "3.11"  # Desired Python version
# UV_VERSION = "0.4.25"  # uv version for standalone binary
# REQUIREMENTS = [
#     "PySide6>=6.5.0",  # PySide6 for GUI
#     # Add other dependencies here, e.g., "requests>=2.28.0"
# ]
#
# def run_command(command, check=True, shell=True):
#     """Run a shell command and handle errors."""
#     try:
#         result = subprocess.run(command, shell=shell, check=check, text=True, capture_output=True)
#         return result
#     except subprocess.CalledProcessError as e:
#         print(f"Error running command: {command}")
#         print(f"Output: {e.stderr}")
#         sys.exit(1)
#     except FileNotFoundError:
#         print(f"Command not found: {command}")
#         sys.exit(1)
#
# def install_uv():
#     """Install uv if not present, using platform-specific methods."""
#     print("Checking for uv...")
#     if run_command("uv --version", check=False).returncode == 0:
#         print("uv is already installed.")
#         return
#
#     print("Installing uv...")
#     system = platform.system().lower()
#     temp_dir = Path(tempfile.gettempdir())
#     uv_binary = temp_dir / ("uv.exe" if system == "windows" else "uv")
#
#     # Platform-specific uv installation
#     if system == "linux" or system == "darwin":  # Linux or macOS
#         # Download standalone uv binary from GitHub releases
#         arch = "x86_64" if platform.machine() == "x86_64" else "arm64"
#         uv_url = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-{arch}-{'linux' if system == 'linux' else 'apple-darwin'}.tar.gz"
#         tar_file = temp_dir / "uv.tar.gz"
#         try:
#             print(f"Downloading uv from {uv_url}...")
#             urllib.request.urlretrieve(uv_url, tar_file)
#             run_command(f"tar -xzf {tar_file} -C {temp_dir}")
#             os.chmod(uv_binary, 0o755)  # Make executable
#         except Exception as e:
#             print(f"Failed to download uv: {e}")
#             print("Trying to install via pip...")
#             run_command("pip install uv")
#     elif system == "windows":
#         # Download Windows uv binary
#         uv_url = f"https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/uv-x86_64-pc-windows-msvc.zip"
#         zip_file = temp_dir / "uv.zip"
#         try:
#             print(f"Downloading uv from {uv_url}...")
#             urllib.request.urlretrieve(uv_url, zip_file)
#             run_command(f"powershell -Command Expand-Archive -Path {zip_file} -DestinationPath {temp_dir}")
#         except Exception as e:
#             print(f"Failed to download uv: {e}")
#             print("Trying to install via pip...")
#             run_command("pip install uv")
#     else:
#         print(f"Unsupported platform: {system}")
#         sys.exit(1)
#
#     # Verify uv installation
#     if uv_binary.exists():
#         os.environ["PATH"] = f"{temp_dir}{os.pathsep}{os.environ.get('PATH', '')}"
#         run_command(f"{uv_binary} --version")
#     else:
#         print("uv installation failed.")
#         sys.exit(1)
#
# def setup_environment():
#     """Set up virtual environment and install dependencies using uv."""
#     print("Setting up virtual environment...")
#
#     # Ensure uv is installed
#     install_uv()
#
#     # Create virtual environment with specific Python version
#     print(f"Creating virtual environment with Python {PYTHON_VERSION}...")
#     run_command(f"uv venv --python {PYTHON_VERSION} {VENV_DIR}")
#
#     # Get virtual environment paths
#     if platform.system() == "Windows":
#         python_bin = Path(VENV_DIR) / "Scripts" / "python.exe"
#         uv_bin = Path(VENV_DIR) / "Scripts" / "uv.exe"
#     else:
#         python_bin = Path(VENV_DIR) / "bin" / "python"
#         uv_bin = Path(VENV_DIR) / "bin" / "uv"
#
#     if not python_bin.exists():
#         print(f"Error: Python not found in virtual environment at {python_bin}")
#         sys.exit(1)
#
#     # Install dependencies using uv
#     print("Installing dependencies...")
#     requirements_str = " ".join(REQUIREMENTS)
#     run_command(f"{uv_bin} pip install {requirements_str}")
#
#     print("Setup complete!")
#
# def is_venv_active():
#     """Check if running inside the virtual environment."""
#     return sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
#
# def run_application():
#     """Run the PySide6 application."""
#     try:
#         from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
#         from PySide6.QtCore import Qt
#     except ImportError:
#         print("Error: PySide6 not installed. Ensure setup completed successfully.")
#         sys.exit(1)
#
#     # Simple PySide6 application
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("PySide6 Example")
#     window.setFixedSize(400, 300)
#
#     # Create a central widget with a layout
#     central_widget = QWidget()
#     window.setCentralWidget(central_widget)
#     layout = QVBoxLayout(central_widget)
#
#     # Add a label
#     label = QLabel("Hello, PySide6!\nThis is a sample application.", alignment=Qt.AlignCenter)
#     layout.addWidget(label)
#
#     window.show()
#     sys.exit(app.exec())
#
# def main():
#     """Main function to handle setup or run."""
#     parser = argparse.ArgumentParser(description="Setup and run a PySide6 application.")
#     parser.add_argument("--setup", action="store_true", help="Run setup to create virtual environment and install dependencies")
#     args = parser.parse_args()
#
#     if args.setup or not is_venv_active():
#         # Run setup if explicitly requested or not in virtual environment
#         setup_environment()
#         # Re-run the script in the virtual environment
#         python_bin = Path(VENV_DIR) / ("Scripts" if platform.system() == "Windows" else "bin") / "python"
#         run_command(f"{python_bin} {__file__}", check=False)
#     else:
#         # Run the application if in virtual environment
#         run_application()
#
# if __name__ == "__main__":
#     main()


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
