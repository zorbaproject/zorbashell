#!/bin/bash


#please run this with sudo
if [ "$(whoami)" == "root" ] ; then
    echo "You're root, good."
else
    echo "Please run this program with sudo."
    exit 1
fi


pip3 install telepot
pip3 install chatterbot

#We should ask for Telegram Token
echo "Please write here your Telegram Bot Token:"
read $token
echo $token > $(pwd)/telegramtoken.txt


cat << EOF > /lib/systemd/system/zorbabot.service
[Unit]
Description=Archimedes bot on Telegram with Zorba CMD
[Service]
ExecStart=$(pwd)/zorbabot.py
StandardOutput=null
[Install]
WantedBy=multi-user.target
Alias=zorbabot.service
EOF

#add line on /etc/crontab for auto update
cronfile="/etc/crontab"
updatefile=$(pwd)"/install/autoupdate-zorbabot.sh"
if grep -q "$updatefile" "$cronfile"; then
echo "00,30 * * * * $updatefile" >> $cronfile
fi

apt-get install tesseract-ocr tesseract-ocr-all
