# digest_utils.py
# outdated global queue logic

import json
import os
from jinja2 import Environment, FileSystemLoader

DIGEST_QUEUE_PATH = "data/digest_queue.json"
SKIPPED_VIDEOS_PATH = "data/skipped_videos.json"
TEMPLATE_PATH = "templates/digest_email.html"


def load_digest_queue():
    if not os.path.exists(DIGEST_QUEUE_PATH):
        return []
    with open(DIGEST_QUEUE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_digest_queue():
    with open(DIGEST_QUEUE_PATH, "w", encoding="utf-8") as f:
        f.write("[]")


def add_to_digest(video_data):
    queue = load_digest_queue()
    queue.append(video_data)
    with open(DIGEST_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def load_skipped_videos():
    if not os.path.exists(SKIPPED_VIDEOS_PATH):
        return []
    with open(SKIPPED_VIDEOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def render_digest_email(digest_videos, skipped_videos):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("digest_email.html")
    return template.render(digest_videos=digest_videos, skipped_videos=skipped_videos)


if __name__ == "__main__":
    # Debug render
    digest = load_digest_queue()
    skipped = load_skipped_videos()
    html = render_digest_email(digest, skipped)
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Preview generated to preview.html")
