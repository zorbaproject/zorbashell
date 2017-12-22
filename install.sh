#!/bin/bash

echo -n "Please specify your preferred language (e.g.: en-US, it-IT, ...) "
read answer
echo $answer > $(dirname $(readlink -f $0))/zorbalanguage.txt

apt-get install -qq python3 python3-dev python-dev python3-pip build-essential swig libpulse-dev w3m w3m-img alsa-utils
pip3 install watchdog

echo -n "Do you want to install speech recognition and sinthesys (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then

/bin/bash $(dirname $(readlink -f $0))/install/install_sphinx-espeak.sh

fi

echo -n "Do you want to install Zorba Telegram Bot (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then

/bin/bash $(dirname $(readlink -f $0))/install/install_zorbabot.sh

fi

