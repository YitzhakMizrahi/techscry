# modules/user_digest.py
import os
import json
from datetime import datetime

USERS_DIR = "users"


def get_digest_path(user_id):
    return os.path.join(USERS_DIR, user_id, "digest_queue.json")


def load_user_digest(user_id):
    path = get_digest_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_user_digest(user_id, items):
    path = get_digest_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def add_to_user_digest(user_id, video):
    digest = load_user_digest(user_id)
    digest.append(video)
    save_user_digest(user_id, digest)


def trim_user_digest(user_id, max_items):
    digest = load_user_digest(user_id)
    trimmed = digest[:max_items]
    save_user_digest(user_id, trimmed)
    return trimmed


def clear_user_digest(user_id):
    save_user_digest(user_id, [])
