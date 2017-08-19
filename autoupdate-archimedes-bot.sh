#!/bin/bash
git pull
systemctl stop archimedes-bot.service
systemctl start archimedes-bot.service
