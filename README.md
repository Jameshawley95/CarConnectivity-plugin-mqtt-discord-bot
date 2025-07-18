# CarConnectivity-DiscordBot

A lightweight bot to monitor and post car charging status updates to Discord using the [carconnectivity-cli](https://github.com/tillsteinbach/CarConnectivity-plugin-mqtt) tool.

## 🔧 Features

- Fetches car charging status from Volkswagen APIs
- Posts live stats to Discord using a webhook
- Pings a role when the car is fully charged (100%)
- Sends a scheduled 9PM update with current charge data

## 📦 Based On

This is a modified standalone fork of the original [`CarConnectivity-CLI`](https://github.com/tillsteinbach/CarConnectivity-plugin-mqtt) project by [@marcelgro](https://github.com/marcelgro).  
All credit to the original author for the base integration.

## ⚙️ Setup

1. Create a `.env` file with:
    ```
    DISCORD_BOT=https://discord.com/api/webhooks/...
    DISCORD_MESSAGE_ID=...
    CAR_BOT_ROLE=...
    ```

2. Run the bot with:
    ```bash
    python main.py
    ```

---

## 📝 Notes

This version is stripped down for Raspberry Pi use and focused purely on Discord integration.
