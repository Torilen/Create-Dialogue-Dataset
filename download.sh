#!/bin/bash

echo "   ____                 __     ___  _      __                     ___       __               __ "
echo "  / __/______ ___  ____/ /    / _ \(_)__ _/ /__  ___ ___ _____   / _ \___ _/ /____ ____ ___ / /_"
echo " / _// __/ -_) _ \/ __/ _ \  / // / / _ \`/ / _ \/ _ \`/ // / -_) / // / _ \`/ __/ _ \`(_-</ -_) __/"
echo "/_/ /_/  \__/_//_/\__/_//_/ /____/_/\_,_/_/\___/\_, /\_,_/\__/ /____/\_,_/\__/\_,_/___/\__/\__/ "
echo "                                               /___/                                            "

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential wget tar zstd python3-pip
sudo pip install langdetect pandas json

echo "Avez-vous déjà le fichier source ? [y/n]"
read cond

if [ ${cond} = "n" ]
then
  echo "Allez sur [http://files.pushshift.io/reddit/comments/] pour y sélectionner un fichier zst"
  echo ">> Copiez l'URL du fichier"
  read reddit_file

  echo ">> Chemin où le fichier sera télechargé"
  read reddit_file_path

  wget ${reddit_file} -O ${reddit_file_path}/reddit_source.zst
  reddit_file_path="$reddit_file_path/reddit_source.zst"
else
  echo "Super ! Dîtes moi où le trouver"
  echo ">> Chemin où le fichier source se trouve"
  read reddit_file_path
fi

echo "Décompression du fichier en cours..."
zstd -d ${reddit_file_path}
echo "end" >> reddit_source



