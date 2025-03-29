import os
import json

USERS_DIR = "users"


def get_all_preferred_channels():
    channels = set()

    for uid in os.listdir(USERS_DIR):
        user_dir = os.path.join(USERS_DIR, uid)
        profile_path = os.path.join(user_dir, "profile.json")

        if os.path.isdir(user_dir) and os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
                preferred = profile.get("interests", {}).get("preferred_channels", [])
                channels.update(preferred)

    return sorted(channels)


if __name__ == "__main__":
    all_channels = get_all_preferred_channels()
    print("📡 Unique channels across all users:")
    for ch in all_channels:
        print("-", ch)
