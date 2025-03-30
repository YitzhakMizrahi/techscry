import os
import sys

# Ensure root directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from agents.email_agent import send_email
from modules.user_profile import load_user_profiles

TEMPLATE_DIR = "templates"
TEMPLATE_DEFAULT = "digest_email.html"
TEMPLATE_EMAIL_SAFE = "digest_email_safe.html"
PREVIEW_HTML = "preview.html"
PREVIEW_SAFE_HTML = "preview_safe.html"

MAX_ITEMS_DEFAULT = 5


def load_user_digest(user_id):
    path = os.path.join("users", user_id, "digest_queue.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_user_digest(user_id, items):
    path = os.path.join("users", user_id, "digest_queue.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def render_digest_email(digest_items, email_safe=False):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template_name = TEMPLATE_EMAIL_SAFE if email_safe else TEMPLATE_DEFAULT
    template = env.get_template(template_name)
    return template.render(digest_items=digest_items, skipped_videos=[])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--email-safe", action="store_true", help="Use email-safe HTML template"
    )
    parser.add_argument(
        "--preview", action="store_true", help="Open email preview in browser"
    )
    parser.add_argument(
        "--max", type=int, default=MAX_ITEMS_DEFAULT, help="Max items per digest email"
    )
    args = parser.parse_args()

    profiles = load_user_profiles()
    if not profiles:
        print("🚫 No user profiles found.")
        return

    for profile in profiles:
        user_id = profile["user_id"]
        digest_items = load_user_digest(user_id)
        if not digest_items:
            print(f"📭 No digest items for user: {user_id}")
            continue

        digest_items.sort(key=lambda x: x.get("score", 0), reverse=True)
        top_items = digest_items[: args.max]

        html = render_digest_email(top_items, email_safe=args.email_safe)

        if args.preview:
            preview_path = PREVIEW_SAFE_HTML if args.email_safe else PREVIEW_HTML
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(html)
            import webbrowser

            webbrowser.open("file://" + os.path.realpath(preview_path))
        else:
            subject = "🗞️ Your TechScry Digest"
            send_email(subject, html, to=profile["email"])
            print(f"📧 Digest sent to {user_id} with {len(top_items)} items.")

            remaining = digest_items[args.max :]
            save_user_digest(user_id, remaining)


if __name__ == "__main__":
    main()
