#!/bin/bash

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
