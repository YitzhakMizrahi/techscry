import os
import json
from datetime import datetime, timedelta

USERS_DIR = "users"
DEFAULT_COOLDOWN_HOURS = 12


def get_last_notified_path(user_id):
    return os.path.join(USERS_DIR, user_id, "last_notified.json")


def is_notification_allowed(user_id, profile):
    cooldown_hours = (
        profile.get("notification_settings", {}).get("cooldown_hours")
        or DEFAULT_COOLDOWN_HOURS
    )
    path = get_last_notified_path(user_id)
    if not os.path.exists(path):
        return True  # never notified before

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            last_sent = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - last_sent >= timedelta(hours=cooldown_hours):
                return True
    except Exception as e:
        print(f"⚠️ Error checking last notification time: {e}")
        return True  # fail open if corrupt

    return False


def update_last_notified(user_id):
    path = get_last_notified_path(user_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.now().isoformat()}, f)


if __name__ == "__main__":
    test_user = "default"
    profile = {"notification_settings": {"cooldown_hours": 6}}
    print("Allowed:", is_notification_allowed(test_user, profile))
    update_last_notified(test_user)
    print("Updated.")
