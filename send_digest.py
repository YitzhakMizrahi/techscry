import json
import os
import webbrowser
import argparse
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
TEMPLATE_DEFAULT = "digest_email.html"
TEMPLATE_EMAIL_SAFE = "digest_email_safe.html"
DIGEST_PATH = "data/digest_queue.json"
SKIPPED_PATH = "data/skipped_videos.json"
PREVIEW_HTML = "preview.html"
PREVIEW_SAFE_HTML = "preview_safe.html"
MOCK_DIGEST_PATH = "mock/mock_digest_data.json"
MOCK_SKIPPED_PATH = "mock/mock_skipped_videos.json"


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_digest_email(digest_items, skipped_videos, email_safe=False):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template_name = TEMPLATE_EMAIL_SAFE if email_safe else TEMPLATE_DEFAULT
    template = env.get_template(template_name)
    return template.render(digest_items=digest_items, skipped_videos=skipped_videos)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use mock data for preview")
    parser.add_argument(
        "--preview", action="store_true", help="Render and preview HTML"
    )
    parser.add_argument(
        "--email-safe", action="store_true", help="Use email-safe HTML template"
    )
    args = parser.parse_args()

    digest_path = MOCK_DIGEST_PATH if args.mock else DIGEST_PATH
    skipped_path = MOCK_SKIPPED_PATH if args.mock else SKIPPED_PATH
    digest_items = load_json(digest_path)
    skipped_videos = load_json(skipped_path)

    print(
        f"🔍 Loaded {len(digest_items)} digest items and {len(skipped_videos)} skipped videos"
    )

    html = render_digest_email(digest_items, skipped_videos, email_safe=args.email_safe)

    if args.preview:
        preview_path = PREVIEW_SAFE_HTML if args.email_safe else PREVIEW_HTML
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("file://" + os.path.realpath(preview_path))
    else:
        if not digest_items and not skipped_videos:
            print("📭 Digest queue is empty. Nothing to send.")
            return

        from agents.email_agent import send_email

        send_email("🗞️ TechScry Digest", html)
        if not args.mock:
            # clear real queue only if this is a real run
            with open(DIGEST_PATH, "w", encoding="utf-8") as f:
                json.dump([], f)
            print("✅ Digest email sent and queue cleared.")


if __name__ == "__main__":
    main()
