import subprocess
import time
import re
import schedule
import threading
import platform
from pathlib import Path
from datetime import datetime

from voluptuous import message
from parse_data import extract_data
from discord_updater import WEBHOOK_URL, send_new_message_with_mention, send_or_update_message

mqtt_exe_path = Path("carconnectivity-mqtt")

config_path = Path("carconnectivity.json")
notified_charge_full = False
last_car_message = ""

def start_regular_loop():
    while True:
        fetch_data()
        print("⏳ Waiting 5 minutes until next update...\n")
        time.sleep(300)

def send_9pm_notification():
    from discord_updater import send_new_message_with_mention
    print("📅 9PM update triggered.")
    if last_car_message:
        send_new_message_with_mention(last_car_message)
    else:
        print("⚠️ No car data to send yet.")
        


def fetch_data():
    global notified_charge_full

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching car data...")

    try:
        
        if platform.system() == "Windows":
            mqtt_exe_path = Path("carconnectivity-mqtt.exe")
            cmd = [str(mqtt_exe_path), str(config_path)]
        else:
            cmd = ["python3", "-m", "carconnectivity_mqtt", str(config_path)]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        time.sleep(10)
        process.terminate()

        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()

        parsed = extract_data(stderr)

        # Build the message content
        lines = ["🚗 **Car Data:**"]
        for k, v in parsed.items():
            lines.append(f"{k}: {v or 'Unknown'}")
        message = "\n".join(lines)
        global last_car_message
        last_car_message = message
        print(message)

        # Check for full charge and ping role if needed
        match = re.search(r"Battery Level:\s*(\d+)", message)
        if not match:
            print("❌ Could not find Battery Level in message, skipping charge logic.")
            send_or_update_message(message)
            return

        charge_level = int(match.group(1))

        # Full charge notification logic
        if charge_level >= 100:
            if not notified_charge_full:
                print("🔔 Car is fully charged, sending role mention...")
                send_new_message_with_mention("Car is fully charged 🔋")
                notified_charge_full = True
        else:
            if charge_level < 100:
                print("🔄 Charge dropped below 100%, resetting notification flag.")
                notified_charge_full = False
            if charge_level < 50:
                print("⚠️ Battery level is below 50%, consider charging soon.")
                send_new_message_with_mention("Battery level is below 50% 🪫")

        send_or_update_message(message)
            

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Schedule the 9PM notification
    schedule.every().day.at("21:00").do(send_9pm_notification)

    # Start the regular 5-min loop in a separate thread
    threading.Thread(target=start_regular_loop, daemon=True).start()

    # Keep the scheduler alive in main thread
    while True:
        schedule.run_pending()
        time.sleep(1)
