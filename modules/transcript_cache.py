# modules/transcript_cache.py
import os
import json
from pathlib import Path

CACHE_DIR = "data/transcript_cache"


def get_transcript_path(video_id):
    return os.path.join(CACHE_DIR, f"{video_id}.json")


def load_cached_transcript(video_id):
    path = get_transcript_path(video_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("transcript")
    return None


def save_transcript_to_cache(video_id, transcript):
    Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
    path = get_transcript_path(video_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"transcript": transcript}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    tid = "abc123"
    sample = "This is a sample transcript."
    save_transcript_to_cache(tid, sample)
    print(load_cached_transcript(tid))
