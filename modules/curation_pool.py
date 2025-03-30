import os
import json
from datetime import datetime


def get_user_curation_path(user_id):
    return os.path.join("users", user_id, "curation_pool.json")


def load_curation_pool(user_id):
    path = get_user_curation_path(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_curation_pool(user_id, pool):
    path = get_user_curation_path(user_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2)


def add_to_curation_pool(user_id, video_data):
    pool = load_curation_pool(user_id)
    video_ids = {entry["video_id"] for entry in pool}

    if video_data["video_id"] in video_ids:
        return  # already added

    entry = {
        "video_id": video_data["video_id"],
        "title": video_data["title"],
        "channel": video_data["channel"],
        "url": video_data["url"],
        "summary": video_data["summary"],
        "score": video_data["score"],
        "added_at": datetime.utcnow().isoformat(),
        "notified": False,
    }
    pool.append(entry)
    save_curation_pool(user_id, pool)
