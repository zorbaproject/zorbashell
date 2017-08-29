#!/bin/bash

echo -n "Do you want to install speech recognition and sinthesys (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then

/bin/bash $(dirname $(readlink -f $0))/install/install_sphinx-espeak.sh

fi

echo -n "Do you want to install Archimedes Telegram Bot (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then

/bin/bash $(dirname $(readlink -f $0))/install/install_archimedes-bot.sh

fi

