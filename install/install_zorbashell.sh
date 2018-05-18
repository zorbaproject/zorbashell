#!/bin/bash

#please run this with sudo
if [ "$(whoami)" == "root" ] ; then
    echo "You're root, good."
else
    echo "Please run this program with sudo."
    exit 1
fi

cat << EOF > /lib/systemd/system/zorbashell.service
[Unit]
Description=Voice assistant with Zorba CMD
[Service]
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/zorbashell.py -v
StandardOutput=null
[Install]
WantedBy=multi-user.target
Alias=zorbashell.service
EOF

systemctl enable zorbashell.service
systemctl start zorbashell.service
