import json
import os
import webbrowser
import argparse
from jinja2 import Environment, FileSystemLoader

from modules.user_profile import load_user_profiles
from agents.email_agent import send_email

TEMPLATE_DIR = "templates"
TEMPLATE_DEFAULT = "digest_email.html"
TEMPLATE_EMAIL_SAFE = "digest_email_safe.html"
PREVIEW_HTML = "preview.html"
PREVIEW_SAFE_HTML = "preview_safe.html"
MOCK_DIGEST_PATH = "mock/mock_digest_data.json"
MOCK_SKIPPED_PATH = "mock/mock_skipped_videos.json"


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


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

    if args.mock:
        digest_items = load_json(MOCK_DIGEST_PATH)
        skipped_videos = load_json(MOCK_SKIPPED_PATH)
        html = render_digest_email(
            digest_items, skipped_videos, email_safe=args.email_safe
        )

        print(
            f"🔍 Loaded {len(digest_items)} digest items and {len(skipped_videos)} skipped videos"
        )

        if args.preview:
            preview_path = PREVIEW_SAFE_HTML if args.email_safe else PREVIEW_HTML
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(html)
            webbrowser.open("file://" + os.path.realpath(preview_path))
        else:
            send_email("🗞️ TechScry Digest (Mock)", html)
            print("✅ Mock digest email sent.")
        return

    users = load_user_profiles()
    if not users:
        print("🚫 No user profiles found.")
        return

    for user in users:
        user_id = user["user_id"]
        email = user.get("email")
        if not email:
            print(f"⚠️ Skipping user '{user_id}' (no email address)")
            continue

        digest_path = os.path.join("users", user_id, "digest_queue.json")
        skipped_path = os.path.join("users", user_id, "skipped.json")

        digest_items = load_json(digest_path)
        skipped_videos = load_json(skipped_path)

        if not digest_items and not skipped_videos:
            print(f"📭 No digest or skipped videos for user '{user_id}'. Skipping.")
            continue

        html = render_digest_email(
            digest_items, skipped_videos, email_safe=args.email_safe
        )
        subject = f"🗞️ TechScry Digest for {user_id}"

        if args.preview:
            preview_path = PREVIEW_SAFE_HTML if args.email_safe else PREVIEW_HTML
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(html)
            webbrowser.open("file://" + os.path.realpath(preview_path))
        else:
            send_email(subject, html, to=email)
            print(f"✅ Digest email sent to {user_id} ({email})")

            # Clear queues after real send
            save_json(digest_path, [])
            save_json(skipped_path, [])
            print(f"🧹 Cleared digest and skipped queues for '{user_id}'")


if __name__ == "__main__":
    main()
