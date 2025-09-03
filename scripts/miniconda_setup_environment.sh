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
user=solubrew
uuid=$(uuidgen)
#===============================================================================||
env=fuh
#===============================================================================||
# This script installs Miniconda (without sudo) and creates a conda environment with Python 3.13.
# Miniconda provides pre-built Python binaries, so no compilation or admin rights are needed.
# Run this in your home directory or a dedicated folder.

# Set variables
MINICONDA_INSTALLER="Miniconda3-latest-Linux-x86_64.sh"
DOWNLOAD_URL="https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER"
INSTALL_DIR="$HOME/miniconda3"
ENV_NAME="$HOME/ENVs/${env}"

# Step 1: Download Miniconda installer
echo "Downloading Miniconda installer..."
wget "$DOWNLOAD_URL"

# Step 2: Install Miniconda to user directory (interactive; accept defaults or customize path)
echo "Installing Miniconda to $INSTALL_DIR... Follow the prompts (press Enter for defaults, type 'yes' to agree)."
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
mkdir -p "$ENV_NAME"
conda create -y -n "$ENV_NAME" python=3.13

# Step 6: Cleanup
rm "$MINICONDA_INSTALLER"
rm -r "${INSTALL_DIR}"

# Instructions for use
echo "Installation complete!"
echo "To activate the environment, run: conda activate $ENV_NAME"
echo "To verify Python version inside the env: python --version"
echo "Deactivate with: conda deactivate"
echo "For persistent setup, add export PATH=\"$INSTALL_DIR/bin:\$PATH\" to your ~/.bashrc and source it."
#=============================Source Materials==================================||
#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


