# skip_cache.py

import json
from pathlib import Path

SKIPPED_PATH = "data/skipped_videos.json"


def load_skipped_videos():
    if not Path(SKIPPED_PATH).exists():
        return []
    with open(SKIPPED_PATH, "r") as f:
        return json.load(f)


def load_skipped_video_ids():
    return {entry["video_id"] for entry in load_skipped_videos()}


def add_to_skipped(video_id, title=None, url=None, channel=None):
    skipped = load_skipped_videos()
    new_entry = {
        "video_id": video_id,
        "title": title or "(unknown title)",
        "url": url or "",
        "channel": channel or "(unknown)",
    }
    if all(v["video_id"] != video_id for v in skipped):
        skipped.append(new_entry)
        Path(SKIPPED_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(SKIPPED_PATH, "w") as f:
            json.dump(skipped, f, indent=2)


def format_skipped_report():
    skipped = load_skipped_videos()
    if not skipped:
        return "✅ No skipped videos to report."

    lines = ["🛑 Skipped Videos (No Transcript):"]
    for v in skipped:
        lines.append("\n-----------------------------")
        lines.append(f"📺 {v['title']} ({v['channel']})")
        lines.append(f"🔗 {v['url']}")
    return "\n".join(lines)


if __name__ == "__main__":
    add_to_skipped(
        "abc123",
        title="Test Title",
        url="https://youtu.be/abc123",
        channel="Test Channel",
    )
    print(format_skipped_report())
