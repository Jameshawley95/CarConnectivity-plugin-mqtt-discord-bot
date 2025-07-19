#!/bin/bash
echo "🔄 Restarting car bot..."
pkill -f car_bot.py
sleep 1
cd ~/CarConnectivity-plugin-mqtt-discord-bot
nohup python3 car_bot.py > car.log 2>&1 &
echo "✅ Car bot restarted."
