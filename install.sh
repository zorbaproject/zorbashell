#!/bin/bash

echo -n "Please specify your preferred language (e.g.: en-US, it-IT, ...) "
read answer
echo $answer > $(dirname $(readlink -f $0))/zorbalanguage.txt


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

