#!/bin/bash
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
#---
#<(META)>:
#	DOCid:
#	name:
#	description: >
#	version: <[version]>
#	path: <[LEXIvrs]><[path]>.yaml
#	outline: <[outline]>
#	authority: <[authority]>
#	security: <[seclvl]>
#	<(WT)>: -32
#===============================================================================||
now=$(date +"%Y%m%d%H%M%S")
user=soluberw
uuid=$(uuidgen)
#===============================================================================||
device_path=/home/${user}/EDN
git_file=/home/${user}/GitFile
env=uh
version=3.12

# Set variables
PYTHON_VERSION="3.13.7"
INSTALL_DIR="$HOME/.local/python-$PYTHON_VERSION"
VENV_DIR="$HOME/ENVs/${env}"
TARBALL="Python-$PYTHON_VERSION.tgz"
DOWNLOAD_URL="https://www.python.org/ftp/python/$PYTHON_VERSION/$TARBALL"
#===============================================================================||
# This script downloads, compiles, and installs Python 3.13.7 from source into a user-local directory
# on a Debian-based Linux system, then creates a virtual environment using it.
# It assumes you have sudo access for installing build dependencies.
# Run this script in your home directory or a dedicated folder.
# Step 1: Install required dependencies (minimal set for building Python)
echo "Installing build dependencies..."
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget tk-dev libbz2-dev

# Step 2: Download Python source
echo "Downloading Python $PYTHON_VERSION source..."
wget "$DOWNLOAD_URL"

# Step 3: Extract the tarball
echo "Extracting source..."
tar -xzf "$TARBALL"

# Step 4: Configure, build, and install to local directory (no sudo needed)
cd "Python-$PYTHON_VERSION"
echo "Configuring build..."
./configure --prefix="$INSTALL_DIR" --enable-optimizations --with-ensurepip=install
echo "Building Python..."
make -j "$(nproc)"
echo "Installing Python to $INSTALL_DIR..."
make install

# Step 5: Create a virtual environment using the new Python
echo "Creating virtual environment at $VENV_DIR..."
"$INSTALL_DIR/bin/python3" -m venv "$VENV_DIR"

# Step 6: Cleanup
cd ..
rm -rf "Python-$PYTHON_VERSION" "$TARBALL"

# Instructions for use
echo "Installation complete!"
echo "To activate the virtual environment, run: source $VENV_DIR/bin/activate"
echo "To verify Python version inside venv: python --version"
echo "Add $INSTALL_DIR/bin to your PATH if needed for system-wide use: export PATH=\"$INSTALL_DIR/bin:\$PATH\""
#=============================Source Materials==================================||

#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


