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
echo 'Hourly' $uuid $now #> EDN/LOGs/cmds/hourly.log
#check if environment exits
#if not create it

source /home/${user}/ENVs/${env}/bin/activate
python -m nchantdoffice
now=$(date +"%Y%m%d%H%M%S")
echo 'Hourly' $uuid $now #>> EDN/LOGs/cmds/hourly.log
#=============================Source Materials==================================||
#===============================:::DNA:::=======================================||
#<(DNA)>:
#	<(WT)>: 32
#	<@[datetime]@>:
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||


