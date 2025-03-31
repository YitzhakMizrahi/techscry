# send_curated_digest.py (patched to use curation_pool)

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from agents.email_agent import send_email
from modules.user_profile import load_user_profiles
from modules.curation_pool import load_curation_pool, save_curation_pool
from modules.skip_cache import load_skipped_videos

TEMPLATE_DIR = "templates"
TEMPLATE_DEFAULT = "digest_email.html"
TEMPLATE_EMAIL_SAFE = "digest_email_safe.html"
PREVIEW_HTML = "preview.html"
PREVIEW_SAFE_HTML = "preview_safe.html"

MAX_ITEMS_DEFAULT = 5


def render_digest_email(digest_items, skipped_videos=None, email_safe=False):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template_name = TEMPLATE_EMAIL_SAFE if email_safe else TEMPLATE_DEFAULT
    template = env.get_template(template_name)
    return template.render(
        digest_items=digest_items, skipped_videos=skipped_videos or []
    )


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
        pool = load_curation_pool(user_id)
        if not pool:
            print(f"📭 No digest items for user: {user_id}")
            continue

        # Sort by score or added_at
        sorted_pool = sorted(pool, key=lambda x: x.get("score", 0), reverse=True)
        top_items = sorted_pool[: args.max]

        skipped_videos = load_skipped_videos(user_id)
        html = render_digest_email(
            top_items, skipped_videos, email_safe=args.email_safe
        )

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

            # Remove sent items from the pool
            remaining = sorted_pool[args.max :]
            save_curation_pool(user_id, remaining)


if __name__ == "__main__":
    main()
