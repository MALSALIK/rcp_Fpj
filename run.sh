#!/bin/bash
shopt -s xpg_echo 

##########################################################
#  SET DEFAUL VARIABLES
HOST=$HOSTNAME

SHORT_DATE=`date '+%Y-%m-%d'`

TIME=`date '+%H%M'`

SCRIPT_TYPE=`basename $0 | cut -d '.' -f1` ##(get the first line of the file )

filenametime1=$(date +"%m%d%Y%H%M%S")
filenametime2=$(date +"%Y-%m-%d %H:%M:%S")
#########################################################
#  SET VARIABLES 


# export PYTHON_SCRIPT_NAME=$(cat config_file.toml | grep 'py_script' | awk -F"=" '{print $2}' | tr -d '"') # get the py_script from config.toml, and remove the quotes
# export SCRIPTS_FOLDER=$(pwd)
# export LOGDIR=$SCRIPTS_FOLDER/log
# export LOG_FILE=${LOGDIR}/${SHELL_SCRIPT_NAME}_${filenametime1}.log
# # GO TO SCRIPT FOLDER AND RUN
# cd ${SCRIPTS_FOLDER}

#########################################################
# : SET LOG RULES

exec > >(tee ${LOG_FILE}) 2>&1


# chmod +x /home/ubuntu/rcp/run.py
chmod +x /app/run.py

#########################################################
# : RUN SCRIPT
# source /home/ubuntu/rcp/3.10-venv/bin/activate
source /app/3.10-venv/bin/activate

mkdir -p /home/ubuntu/rcp/data

echo "Start to run Python Script"
# python3 ${SCRIPTS_FOLDER}/${PYTHON_SCRIPT_NAME}
# python3 /home/ubuntu/rcp/run.py
python3 /app/run.py


RC1=$?
if [ ${RC1} != 0 ]; then
	echo "PYTHON RUNNING FAILED"
	echo "[ERROR:] RETURN CODE:  ${RC1}"
	echo "[ERROR:] REFER TO THE LOG FOR THE REASON FOR THE FAILURE."
	exit 1
fi

echo "PROGRAM SUCCEEDED"

deactivate

exit 0 