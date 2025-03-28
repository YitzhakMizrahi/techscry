# skip_cache.py

import json
from pathlib import Path

SKIPPED_PATH = "data/skipped_videos.json"


def load_skipped_video_ids():
    if not Path(SKIPPED_PATH).exists():
        return set()
    with open(SKIPPED_PATH, "r") as f:
        return set(json.load(f))


def add_to_skipped(video_id):
    skipped = load_skipped_video_ids()
    skipped.add(video_id)
    Path(SKIPPED_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(SKIPPED_PATH, "w") as f:
        json.dump(sorted(list(skipped)), f, indent=2)


if __name__ == "__main__":
    # Test append
    add_to_skipped("test_video_id")
    print(load_skipped_video_ids())
