import feedparser
import json
from datetime import datetime
from pathlib import Path

from modules.skip_cache import load_skipped_video_ids

CONFIG_PATH = "control_plane/config.yaml"
SEEN_CACHE_DIR = "users"


def get_seen_path(user_id):
    return Path(SEEN_CACHE_DIR) / user_id / "seen_videos.json"


def load_seen_video_ids(user_id):
    seen_path = get_seen_path(user_id)
    if not seen_path.exists():
        return set()
    with open(seen_path, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_seen_video_ids(user_id, video_ids):
    seen_path = get_seen_path(user_id)
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    with open(seen_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(video_ids)), f, indent=2)


def fetch_new_videos(rss_urls, user_id):
    seen_ids = load_seen_video_ids(user_id)
    skipped_ids = load_skipped_video_ids(user_id)
    new_videos = []

    for channel in rss_urls:
        feed = feedparser.parse(channel["rss"])
        for entry in feed.entries:
            video_id = entry.yt_videoid
            if video_id not in seen_ids and video_id not in skipped_ids:
                new_videos.append(
                    {
                        "channel": channel["name"],
                        "video_id": video_id,
                        "title": entry.title,
                        "url": entry.link,
                        "published": entry.published,
                    }
                )

    return new_videos
