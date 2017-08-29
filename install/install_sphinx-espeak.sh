#!/bin/sh

#please run this with sudo
if [ "$(whoami)" == "root" ] ; then
    echo "You're root, good."
else
    echo "Please run this program with sudo."
    exit 1
fi

apt-get install portaudio19-dev
apt-get install -qq python3 python-dev python3-pip build-essential swig libpulse-dev
apt-get install pocketsphinx sphinxtrain
pip3 install --upgrade pip
pip3 install SpeechRecognition
pip3 install PyAudio
pip3 install pocketsphinx

sudo apt-get install mbrola
#on a Raspberry:
#wget http://steinerdatenbank.de/software/mbrola3.0.1h_armhf.deb
#dpkg -i wget mbrola3.0.1h_armhf.deb

#apt-get install mbrola-it3 mbrola-it4
sudo apt-get install espeak

#today pico is not better than mbrola, but in future we could use 
#sudo apt-get install libttspico-utils
#pico2wave -l=it-IT -w=/tmp/test.wav 'prova';aplay /tmp/test.wav;rm /tmp/test.wav

echo -n "Do you want to install it-IT language (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then

/bin/bash $(dirname $(readlink -f $0))/locale-it-IT-install.sh

fi
