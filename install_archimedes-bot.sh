#!/bin/bash

#please run this with sudo
if [ "$(whoami)" == "root" ] ; then
    echo "You're root, good."
else
    echo "Please run this program with sudo."
    exit 1
fi


#We should ask for Telegram Token
echo "Please write here your Telegram Bot Token:"
read $token
echo $token > $(pwd)/telegramtoken.txt


cat << EOF > /lib/systemd/system/archimedes-bot.service
[Unit]
Description=Archimedes bot on Telegram with Zorba CMD
[Service]
ExecStart=$(pwd)/archimedes-bot.py
StandardOutput=null
[Install]
WantedBy=multi-user.target
Alias=archimedes-bot.service
EOF

#add line on /etc/crontab for auto update
cronfile="/etc/crontab"
updatefile=$(pwd)"/autoupdate-archimedes-bot.sh"
if grep -q "$updatefile" "$cronfile"; then
echo "00,30 * * * * $updatefile" >> $cronfile
fi
