# modules/notification_guard.py

import os
import json
from datetime import datetime, timedelta

USERS_DIR = "users"
TIMESTAMP_FILE = "last_notified.json"


def get_timestamp_path(user_id):
    return os.path.join(USERS_DIR, user_id, TIMESTAMP_FILE)


def get_last_notification_time(user_id):
    path = get_timestamp_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return datetime.fromisoformat(data.get("last_sent"))


def update_last_notification_time(user_id):
    path = get_timestamp_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_sent": datetime.now().isoformat()}, f)


def can_send_notification(user_id, cooldown_hours):
    last_time = get_last_notification_time(user_id)
    if not last_time:
        return True  # Never sent before
    return datetime.now() - last_time >= timedelta(hours=cooldown_hours)


if __name__ == "__main__":
    user = "default"
    cooldown = 12
    if can_send_notification(user, cooldown):
        print(f"✅ Cooldown passed, send email to {user}.")
        update_last_notification_time(user)
    else:
        print(f"⏳ Still in cooldown period for {user}.")
