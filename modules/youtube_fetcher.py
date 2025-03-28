# youtube_fetcher.py

import feedparser
import json
from datetime import datetime
from pathlib import Path

from modules.skip_cache import load_skipped_video_ids

CONFIG_PATH = "control_plane/config.yaml"
SEEN_CACHE_PATH = "data/seen_videos.json"


def load_seen_video_ids():
    if not Path(SEEN_CACHE_PATH).exists():
        return set()
    with open(SEEN_CACHE_PATH, "r") as f:
        return set(json.load(f))


def save_seen_video_ids(video_ids):
    Path(SEEN_CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_CACHE_PATH, "w") as f:
        json.dump(sorted(list(video_ids)), f, indent=2)


def fetch_new_videos(rss_urls):
    seen_ids = load_seen_video_ids()
    skipped_ids = load_skipped_video_ids()
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
