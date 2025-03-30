# skip_cache.py (patched for per-user support)

import json
from pathlib import Path


def get_skipped_path(user_id):
    return Path(f"users/{user_id}/skipped.json")


def load_skipped_videos(user_id):
    path = get_skipped_path(user_id)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_skipped_video_ids(user_id):
    return {entry["video_id"] for entry in load_skipped_videos(user_id)}


def add_to_skipped(user_id, video_id, title=None, url=None, channel=None):
    skipped = load_skipped_videos(user_id)
    new_entry = {
        "video_id": video_id,
        "title": title or "(unknown title)",
        "url": url or "",
        "channel": channel or "(unknown)",
    }
    if all(v["video_id"] != video_id for v in skipped):
        skipped.append(new_entry)
        path = get_skipped_path(user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(skipped, f, indent=2)


def format_skipped_report(user_id):
    skipped = load_skipped_videos(user_id)
    if not skipped:
        return "✅ No skipped videos to report."

    lines = ["🛑 Skipped Videos (No Transcript):"]
    for v in skipped:
        lines.append("\n-----------------------------")
        lines.append(f"📺 {v['title']} ({v['channel']})")
        lines.append(f"🔗 {v['url']}")
    return "\n".join(lines)


if __name__ == "__main__":
    test_user = "default"
    add_to_skipped(
        test_user,
        "abc123",
        title="Test Title",
        url="https://youtu.be/abc123",
        channel="Test Channel",
    )
    print(format_skipped_report(test_user))
