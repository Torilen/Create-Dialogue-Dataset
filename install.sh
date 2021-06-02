#!/bin/bash

echo "   ____         __       ____     __  _             _______  ___ "
echo "  /  _/__  ___ / /____ _/ / /__ _/ /_(_)__  ___    / __/ _ \/ _ \ "
echo " _/ // _ \(_-</ __/ _ \`/ / / _ \`/ __/ / _ \/ _ \  / _// // / // /"
echo "/___/_//_/___/\__/\_,_/_/_/\_,_/\__/_/\___/_//_/ /_/ /____/____/ "

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential wget tar zstd python3-pip
sudo pip install langdetect pandas json