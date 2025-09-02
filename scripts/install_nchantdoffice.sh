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
#===============================================================================||
echo 'Hourly' $uuid $now #> EDN/LOGs/cmds/hourly.log
#check if environment exits
#if not create it

rm -r /home/${user}/ENVs/${env}
rm -r /home/${user}/.config/python_keyring

mkdir -p /home/${user}/ENVs/${env}

python${version} -m venv /home/${user}/ENVs/${env}
source /home/${user}/ENVs/${env}/bin/activate

pip cache purge
pip install --upgrade pip

pip install keyring
keyring --disable

pip install --upgrade  -r ${device_path}/Downloads/requirements
pip install --upgrade  -r ${device_path}/Downloads/full_requirements


#Create applications directory if it doesn't exist
mkdir -p /home/${user}/.local/share/applications
touch /home/${user}/.local/share/applications/nchantdoffice.desktop

#Create icon directory if it doesn't exist
mkdir -p /home/${user}/.local/share/nchantdoffice
cp ${device_path}/Downloads/launch_icon.svg /home/${user}/.local/share/nchantdoffice

#make desktop launcher
echo "[Desktop Entry]
Version=0.0.1.0.1.1
Name=Nchantd Office
Exec=bash ${device_path}/cmds/launch_nchantdoffice.sh
Icon=/home/${user}/.local/share/nchantdoffice/launch_icon.svg
Type=Application
Terminal=false
Categories=Office;Utility;
StartupNotify=true" > /home/${user}/.local/share/applications/nchantdoffice.desktop

#Make desktop file executable
chmod +x /home/${user}/.local/share/applications/nchantdoffice.desktop


pip install --upgrade git+file://${git_file}/condor.git@dev
pip install --upgrade git+file://${git_file}/subtrix.git@dev
pip install --upgrade git+file://${git_file}/squirl.git@dev
pip install --upgrade git+file://${git_file}/pycurity.git@dev
pip install --upgrade git+file://${git_file}/pyularity.git@dev
pip install --upgrade git+file://${git_file}/nchantrs.git@dev
pip install --upgrade git+file://${git_file}/pyside6pandas.git@dev
pip install --upgrade git+file://${git_file}/sentinel.git@dev
pip install --upgrade git+file://${git_file}/apig.git@dev
pip install --upgrade git+file://${git_file}/micromole.git@dev
pip install --upgrade git+file://${git_file}/twof.git@dev
pip install --upgrade git+file://${git_file}/worldbridge.git@dev
pip install --upgrade git+file://${git_file}/ogma.git@dev
pip install --upgrade git+file://${git_file}/pyffice.git@dev
pip install --upgrade git+file://${git_file}/nchantdoffice.git@dev

python -m nchantdoffice setup
now=$(date +"%Y%m%d%H%M%S")
echo 'Hourly' $uuid $now #>> EDN/LOGs/cmds/hourly.log
#=============================Source Materials==================================||


#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


