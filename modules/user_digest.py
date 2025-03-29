# modules/user_digest.py

import os
import json

USER_DATA_DIR = "users"


def get_user_digest_path(user_id):
    return os.path.join(USER_DATA_DIR, user_id, "digest_queue.json")


def load_user_digest(user_id):
    path = get_user_digest_path(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def add_to_user_digest(user_id, item):
    digest = load_user_digest(user_id)
    digest.append(item)
    path = get_user_digest_path(user_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(digest, f, indent=2)


def clear_user_digest(user_id):
    path = get_user_digest_path(user_id)
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)


def has_user_digest_content(user_id):
    return bool(load_user_digest(user_id))
