#!/bin/bash
line=$(less /lib/systemd/system/archimedes-bot.service | grep "ExecStart=")
folder=${line:10}
cd $folder
git pull
systemctl stop archimedes-bot.service
systemctl start archimedes-bot.service
