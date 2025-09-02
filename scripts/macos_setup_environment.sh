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

#!/bin/bash

# This script installs Miniconda (without admin privileges) and creates a conda environment with Python 3.13 on macOS.
# It detects the architecture (Intel x86_64 or Apple Silicon arm64) automatically.
# Run this in your home directory or a dedicated folder.

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    MINICONDA_INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
else
    MINICONDA_INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
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

# Optional: Add to .bash_profile or .zshrc for permanent PATH (uncomment and adjust for your shell)
# echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bash_profile
# source ~/.bash_profile

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
echo "For persistent setup, add export PATH=\"$INSTALL_DIR/bin:\$PATH\" to your shell profile (e.g., ~/.bash_profile or ~/.zshrc) and source it."
#=============================Source Materials==================================||

#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


