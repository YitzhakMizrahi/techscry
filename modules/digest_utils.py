# digest_utils.py

import json
from pathlib import Path
from modules.skip_cache import load_skipped_videos

DIGEST_PATH = "data/digest_queue.json"


def load_digest_queue():
    if not Path(DIGEST_PATH).exists():
        return []
    with open(DIGEST_PATH, "r") as f:
        return json.load(f)


def add_to_digest(video_info):
    queue = load_digest_queue()
    queue.append(video_info)
    Path(DIGEST_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(DIGEST_PATH, "w") as f:
        json.dump(queue, f, indent=2)


def clear_digest_queue():
    if Path(DIGEST_PATH).exists():
        Path(DIGEST_PATH).unlink()


def format_digest_email(queue):
    lines = ["🗞️ TechScry Daily Digest"]

    if not queue:
        lines.append("\n(No high-interest content today.)")
    else:
        for entry in queue:
            lines.append("\n-----------------------------")
            lines.append(f"📺 {entry['title']} ({entry['channel']})")
            lines.append(f"🔗 {entry['url']}")
            lines.append(f"📝 Summary:\n{entry['summary']}")

    skipped = load_skipped_videos()
    if skipped:
        lines.append("\n\n🚫 Skipped Videos (No Transcript):")
        for s in skipped:
            lines.append("\n-----------------------------")
            lines.append(f"📺 {s['title']} ({s['channel']})")
            lines.append(f"🔗 {s['url']}")

    return "\n".join(lines)


if __name__ == "__main__":
    test_video = {
        "title": "Test Video",
        "channel": "OpenAI",
        "url": "https://youtu.be/test",
        "summary": "This is a fake summary.",
    }
    add_to_digest(test_video)
    print(format_digest_email(load_digest_queue()))
