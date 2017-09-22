#!/bin/bash
line=$(less /lib/systemd/system/zorbabotbot.service | grep "ExecStart=")
folder=${line:10}
cd $folder
git pull
systemctl stop zorbabot.service
systemctl start zorbabot.service
