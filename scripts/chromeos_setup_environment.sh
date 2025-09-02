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

# This script installs Miniconda (without admin privileges) and creates a conda environment with Python 3.13 on ChromeOS.
# It runs in the Linux development environment (Crostini/Penguin terminal). Enable it first in ChromeOS Settings > Advanced > Developers > Linux development environment.
# Detects architecture (x86_64 or aarch64) automatically.
# Run this in your home directory or a dedicated folder.

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
elif [ "$ARCH" = "aarch64" ]; then
    MINICONDA_INSTALLER="Miniconda3-latest-Linux-aarch64.sh"
else
    echo "Unsupported architecture: $ARCH. Exiting."
    exit 1
fi

# Set variables
DOWNLOAD_URL="https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"
INSTALL_DIR="$HOME/miniconda3"
ENV_NAME="my_python_313_env"

# Step 1: Download Miniconda installer
echo "Downloading Miniconda installer for $ARCH..."
curl -O "$DOWNLOAD_URL"

# Step 2: Install Miniconda to user directory (batch mode, no prompts)
echo "Installing Miniconda to $INSTALL_DIR..."
bash "$MINICONDA_INSTALLER" -b -p "$INSTALL_DIR"

# Step 3: Initialize conda (add to PATH for this session)
echo "Initializing conda..."
source "$INSTALL_DIR/bin/activate"

# Optional: Add to .bashrc for permanent PATH (uncomment if needed)
# echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
# source ~/.bashrc

# Step 4: Update conda (optional but recommended)
echo "Updating conda..."
conda update -y -n base conda

# Step 5: Create a conda environment with Python 3.13
echo "Creating conda environment '$ENV_NAME' with Python 3.13..."
conda create -y -n "$ENV_NAME" python=3.13

# Step 6: Cleanup
rm "$MINICONDA_INSTALLER"

# Instructions for use
echo "Installation complete!"
echo "To activate the environment, run: conda activate $ENV_NAME"
echo "To verify Python version inside the env: python --version"
echo "Deactivate with: conda deactivate"
echo "For persistent setup, add export PATH=\"$INSTALL_DIR/bin:\$PATH\" to your ~/.bashrc and source it."
echo "Note: Run this in the Linux (Penguin) terminal on ChromeOS."
#=============================Source Materials==================================||

#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


