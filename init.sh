#!/bin/bash

# install specific python version to make sure all the work env for various server are the same.

sudo apt-get update
sudo apt install python3.10 -y
# sudo apt install python3.10-distutils -y

install awscli
sudo apt  install awscli -y
sudo apt install python3-pip -y
# Create a virtual environment for specific python3.8 version
sudo apt install python3.10-venv -y
# # virtualenv --python="/usr/bin/python3.8" sandbox  
# # source sandbox/bin/activate 
python3 -m venv 3.10-venv
source 3.10-venv/bin/activate
# Install dependencies
pip install -r requirements.txt



chmod a+x run.sh # make run.sh executable

mkdir -p log # create log directory if it doesn't exist