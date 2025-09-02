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
# This PowerShell script downloads and installs Python 3.13.7 using the official Windows installer
# into a user-local directory on Windows 11, without requiring admin rights (per-user install).
# It then creates a virtual environment using the installed Python.
# Run this script in PowerShell as a regular user.
# Assumes 64-bit Windows; for 32-bit, change the URL to python-3.13.7.exe (non-amd64).

# Set variables
$PYTHON_VERSION = "3.13.7"
$INSTALL_DIR = "$env:USERPROFILE\.local\python-$PYTHON_VERSION"
$VENV_DIR = "$env:USERPROFILE\my_python_313_venv"
$INSTALLER = "python-$PYTHON_VERSION-amd64.exe"
$DOWNLOAD_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/$INSTALLER"

# Step 1: Download the Python installer
Write-Output "Downloading Python $PYTHON_VERSION installer..."
Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile $INSTALLER

# Step 2: Install Python silently to local directory (per-user, no admin needed)
Write-Output "Installing Python to $INSTALL_DIR..."
& .\$INSTALLER /quiet InstallAllUsers=0 TargetDir="$INSTALL_DIR" PrependPath=0 Include_pip=1 Include_test=0 Include_doc=0

# Step 3: Create a virtual environment using the new Python
Write-Output "Creating virtual environment at $VENV_DIR..."
& "$INSTALL_DIR\python.exe" -m venv $VENV_DIR

# Step 4: Cleanup
Remove-Item $INSTALLER

# Instructions for use
Write-Output "Installation complete!"
Write-Output "To activate the virtual environment, run: $VENV_DIR\Scripts\Activate.ps1"
Write-Output "To verify Python version inside venv: python --version"
Write-Output "Add $INSTALL_DIR to your PATH if needed for system-wide use: `$env:PATH = `"$INSTALL_DIR;`$env:PATH`""
#=============================Source Materials==================================||

#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


