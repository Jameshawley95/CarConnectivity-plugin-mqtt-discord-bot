import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_BOT")
MESSAGE_ID = os.getenv("DISCORD_MESSAGE_ID")
DISCORD_MESSAGE_FILE = ".discord_message_id"
ROLE_ID = os.getenv("CAR_BOT_ROLE")

def update_env_variable(key, value):
    lines = []
    found = False
    with open(".env", "r") as f:
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"{key}={value}\n")
    with open(".env", "w") as f:
        f.writelines(lines)

def send_new_message_with_mention(content):
    role_id = os.getenv("CAR_BOT_ROLE")
    if not role_id:
        print("⚠️ No CAR_BOT_ROLE defined.")
        return

    message = f"<@&{role_id}>\n{content}"
    webhook_base = WEBHOOK_URL.split("/messages")[0]

    resp = requests.post(f"{webhook_base}?wait=true", json={"content": message})
    if resp.ok:
        print("✅ 9PM role message sent successfully.")
    else:
        print(f"❌ Failed to send 9PM message → {resp.status_code} {resp.text}")

def send_or_update_message(content, charging_complete=False):
    message_id = MESSAGE_ID
    full_message = f"{content}"

    # Try to PATCH the existing message
    if message_id:
        edit_url = f"{WEBHOOK_URL}/messages/{message_id}"
        resp = requests.patch(edit_url, json={"content": full_message})
        if resp.ok:
            print("✅ Updated existing Discord message.")
            return
        else:
            print(f"⚠️ Patch failed → {resp.status_code} {resp.text}")
            print("Creating a new message instead...")

    # If no message ID or patch failed, POST a new message
    webhook_base = WEBHOOK_URL.split("/messages")[0]
    post_resp = requests.post(f"{webhook_base}?wait=true", json={"content": full_message})

    if post_resp.ok:
        try:
            new_message_id = post_resp.json()["id"]
            print("✅ Message created successfully.")
            print(f"🔄 Updating .env with: DISCORD_MESSAGE_ID={new_message_id}")
            update_env_variable("DISCORD_MESSAGE_ID", new_message_id)
        except Exception:
            print("⚠️ Message sent but failed to parse JSON. Please update .env manually.")
    else:
        print(f"❌ Failed to send new message → {post_resp.status_code} {post_resp.text}")
