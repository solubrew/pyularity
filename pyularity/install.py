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
from os.path import abspath, dirname, join, exists
from os import makedirs
import sys
import subprocess
from pathlib import Path
import urllib
import zipfile

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pycurity.pyvice import Device
from pyularity.download import download_python

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "launch.yaml")


class Package(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("Package").override(cfg)
        self.application = None
        self.is_executable = None
        self.path = None
        self.python_executeable = None
        self.device = Device()
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
        download_python(path, platform, version)
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
        download_python(path, platform, version)
        # Specifically tailored for macOS package
        subprocess.run(["sudo", "installer", "-pkg", str(python_archive), "-target", "/"])
        return self

    def install_python_windows(self):
        """"""
        download_python(path, platform, version)
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

    def install_via_pip(self):
        """Install the pip package manager."""
        return self

    def install_via_pip_git(self):
        """"""
        return self

    def install_via_pip_git_local(self):
        """"""
        for package, branch in self.modules.items():
            file_ = f"git+file:///{package}.git@{branch}"
            cmd = [self.python_executeable, "-m", "pip", "install", "--upgrade", file_]
            subprocess.run(cmd, check=True)
        return self

    def install_via_pip_local(self):
        """"""
        return self

    def set_packages(self):
        """"""
        self.packages = self.config.dikt.get("packages", {})
        return self

    def create_virtual_environment_path(self):
        """"""
        if self.device.system.lower() == "linux":
            self.venv_path = Path(f"~/.local/share/{self.application}/python")
        elif self.device.system.lower() == "windows":
            self.venv_path = Path(f"~\\{self.application}\\python")
        elif self.device.system.lower() == "macos":
            self.venv_path = Path(f"~/Library/Application Support/{self.application}/python")
        elif self.device.system.lower() == "chromeos":
            self.venv_path = Path(f"~/opt/{self.application}/python")
        else:
            print(f"Unsupported platform! {self.device.system}")
            sys.exit(1)
        makedirs(self.venv_path, exist_ok=True)
        return self

    def setup_virtual_environment(self):
        """"""
        logma.info("Setting up virtual environment...")
        self.create_virtual_environment_path()
        if self.device.system.lower() == "linux":
            try:
                cmd = [f"virtualenv", "-p=/usr/bin/python{self.PYTHON_VERSION}", self.venv_path]
                subprocess.run(cmd, check=True, text=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                logma.error(f"Error setting up virtual environment: {e}")
                return None
            except FileNotFoundError:
                logma.error("Python not found. Please install Python and try again.")
                return None
        elif self.device.system.lower() == "windows":
            try:
                cmd = [f"virtualenv", "-p=/usr/bin/python{self.PYTHON_VERSION}", self.venv_path]
                subprocess.run(cmd, check=True, text=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                logma.error(f"Error setting up virtual environment: {e}")
                return None
            except FileNotFoundError:
                logma.error("Python not found. Please install Python and try again.")
                return None
        elif self.device.system.lower() == "macos":
            try:
                cmd = [f"virtualenv", "-p=/usr/bin/python{self.PYTHON_VERSION}", self.venv_path]
                subprocess.run(cmd, check=True, text=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                logma.error(f"Error setting up virtual environment: {e}")
                return None
            except FileNotFoundError:
                logma.error("Python not found. Please install Python and try again.")
                return None
        elif self.device.system.lower() == "chromeos":
            try:
                cmd = [f"virtualenv", "-p=/usr/bin/python{self.PYTHON_VERSION}", self.venv_path]
                subprocess.run(cmd, check=True, text=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                logma.error(f"Error setting up virtual environment: {e}")
                return None
            except FileNotFoundError:
                logma.error("Python not found. Please install Python and try again.")
                return None
        else:
            print(f"Unsupported platform! {self.device.system}")
            sys.exit(1)

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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
