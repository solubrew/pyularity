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
from os.path import abspath, dirname, join
import datetime as dt
import os
import sys
import platform
import urllib.request
import subprocess
import tarfile
import zipfile
from pathlib import Path

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pyularity.yaml")


class Package(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("Package").override(cfg)
        self.application = None
        self.is_executable = None
        self.path = None
        self.system = None
        self.packages = None
        self.version = None
        self.set_packages()
        self.set_version()

    def check_install(self):
        """"""
        return self

    def check_package_hash(self):
        """"""
        return self

    def check_run_method(self):
        """"""
        if sys.argv[0].endswith(".py"):
            self.is_executable = False
        elif hasattr(sys, "frozen"):
            self.is_executable = True
        else:
            self.is_executable = True
        return self

    def create_virtual_environment(self):
        """"""
        return self

    def get_package_install_manifest(self):
        """"""
        return self

    def install_python(self, application, version="3.12.3"):
        """Download and set up Python interpreter if not already installed."""
        self.check_run_method()
        self.system = platform.system().lower()
        self.application = application
        self.set_install_path(version)
        if self.is_executable:
            # URLs based on system
            python_url = None
            if self.system == "windows":
                self.install_python_windows()
            elif self.system == "linux":
                self.install_python_linux()
            elif self.system == "darwin":  # macOS
                self.install_python_macos()
            else:
                print("Unsupported platform!")
                sys.exit(1)
        print(f"Python set up successfully in {python_dir}")
        return python_dir

    def install_python_linux(self):
        """"""
        python_url = f"https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
        python_archive = self.path / "Python.tgz"
        download_file(python_url, str(python_archive))
        extract_archive(str(python_archive), python_dir)
        # Compilation or setup may be needed on Linux
        python_source_dir = python_dir / f"Python-{version}"
        subprocess.run(["./configure"], cwd=python_source_dir)
        subprocess.run(["make"], cwd=python_source_dir)
        subprocess.run(["make", "install"], cwd=python_source_dir)
        # sudo apt-get install libqt5-dev
        return self

    def install_python_linux_debian(self):
        """"""

    def isntall_python_linux_arch(self):
        """"""

    def install_python_macos(self):
        """"""
        # TODO need to integrate hash checking
        python_url = f"https://www.python.org/ftp/python/{version}/python-{version}-macos11.pkg"
        python_archive = self.path / "python.pkg"
        download_file(python_url, str(python_archive))
        # Specifically tailored for macOS package
        subprocess.run(["sudo", "installer", "-pkg", str(python_archive), "-target", "/"])
        return self

    def install_python_windows(self):
        """"""
        python_url = f"https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip"
        python_archive = self.path / "python-embed.zip"
        download_file(python_url, str(python_archive))
        extract_archive(str(python_archive), python_dir)
        return self

    def install_uv(self):
        """Install the UV package manager."""
        print("Installing UV package manager...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        except subprocess.CalledProcessError:
            print("Failed to install UV.")
            sys.exit(1)
        print("UV installed successfully!")
        return self

    def install_required_packages(self, packages):
        """Install required Python packages using UV."""
        print("Installing packages using UV...")
        for pkg in packages:
            # TODO need to check the package hash before install
            print(f"Installing {pkg}...")
            try:
                subprocess.run(["uv", "install", pkg], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to install {pkg}")
        print("All packages installed.")
        return self

    def set_install_path(self, path):
        """"""
        # Determine Python URL and paths
        python_dir = Path(f".local/share/{self.application}/python")
        if python_dir.exists():
            print("Python is already installed.")
            return python_dir  # Assume Python was set up in the same directory before
        python_dir.mkdir(parents=True, exist_ok=True)  # Create installation directory
        print(f"Setting up Python for {system}...")
        return self

    def set_environment_path(self, path):
        """"""
        return self

    def set_packages(self):
        """"""
        self.packages = self.config.dikt.get("packages", {})
        return self

    def set_version(self):
        """"""
        self.version = self.config.dikt.get("version", {})
        return self

    def update_database(self, version_from, version_to):
        """"""
        # TODO: need to hand updates to the applications update process

    def update_packages(self, version_from, version_to):
        """"""
        return self


class Run(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("Run").override(cfg)
        self.args = None

    def run(self, args):
        """"""
        self.args = args
        return self


def download_file(url: str, output_path: str):
    """Download a file from a URL into a specific location."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, output_path)
    print(f"Downloaded file to {output_path}")


def extract_archive(file_path: str, extract_to: str):
    """Extract a .zip or .tar.gz archive."""
    print(f"Extracting {file_path} to {extract_to}...")
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.endswith(".tar.gz"):
        with tarfile.open(file_path, "r:gz") as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        print("Unsupported archive format!")
        sys.exit(1)
    print(f"Extraction complete: {extract_to}")


def main():
    print("Starting self-contained Python installer...")
    # Step 1: Set up Python environment
    python_dir = setup_python()
    if not python_dir:
        sys.exit("Could not set up Python!")
    # Ensure Python executable points to the newly installed one
    python_executable = python_dir / ("python.exe" if platform.system().lower() == "windows" else "python3")
    if python_executable.exists():
        sys.executable = str(python_executable)
    else:
        print("Error: Python executable not found after installation.")
        sys.exit(1)
    print("Installation complete! You can now use Python and your packages.")


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
