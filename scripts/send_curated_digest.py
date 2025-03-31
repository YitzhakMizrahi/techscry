# send_curated_digest.py (patched with --log-only, --save-html, structured logging)

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.email_agent import send_email
from modules.user_profile import load_user_profiles
from modules.curation_pool import load_curation_pool, save_curation_pool
from modules.skip_cache import load_skipped_videos
from utils.notification_gate import is_notification_allowed, update_last_notified

TEMPLATE_DIR = "templates"
TEMPLATE_DEFAULT = "digest_email.html"
TEMPLATE_EMAIL_SAFE = "digest_email_safe.html"
PREVIEW_HTML = "preview.html"
PREVIEW_SAFE_HTML = "preview_safe.html"
DIGEST_LOG_PATH = "logs/pipeline_log.jsonl"
DIGEST_SAVE_DIR = "digests"
MAX_ITEMS_DEFAULT = 5


def render_digest_email(digest_items, skipped_videos=None, email_safe=False):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template_name = TEMPLATE_EMAIL_SAFE if email_safe else TEMPLATE_DEFAULT
    template = env.get_template(template_name)
    return template.render(
        digest_items=digest_items, skipped_videos=skipped_videos or []
    )


def log_digest_attempt(
    user_id, items, mode="real", status="executed", cooldown_active=False
):
    os.makedirs(os.path.dirname(DIGEST_LOG_PATH), exist_ok=True)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user_id,
        "action": "send_digest",
        "mode": mode,
        "status": status,
        "items": len(items),
        "cooldown_active": cooldown_active,
    }
    with open(DIGEST_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def save_digest_html(user_id, html, email_safe=False):
    os.makedirs(DIGEST_SAVE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat().replace(":", "-")
    suffix = "safe" if email_safe else "styled"
    filename = f"{user_id}_{timestamp}_{suffix}.html"
    path = os.path.join(DIGEST_SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 Saved digest for {user_id} → {filename}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--email-safe", action="store_true", help="Use email-safe HTML template"
    )
    parser.add_argument(
        "--preview", action="store_true", help="Open email preview in browser"
    )
    parser.add_argument(
        "--log-only", action="store_true", help="Don't actually send emails"
    )
    parser.add_argument(
        "--save-html", action="store_true", help="Save digest HTML per user"
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

        cooldown_ok = is_notification_allowed(user_id, profile)
        if not cooldown_ok and not args.log_only:
            print(f"⏳ Cooldown active for user '{user_id}', skipping.")
            log_digest_attempt(
                user_id,
                pool[: args.max],
                mode="real",
                status="skipped",
                cooldown_active=True,
            )
            continue

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
            log_digest_attempt(user_id, top_items, mode="preview", status="previewed")

        elif args.log_only:
            print(
                f"📝 Would send digest to {user_id} with {len(top_items)} items (log-only mode)"
            )
            log_digest_attempt(user_id, top_items, mode="log_only", status="previewed")

        else:
            subject = "🗞️ Your TechScry Digest"
            send_email(subject, html, to=profile["email"])
            print(f"📧 Digest sent to {user_id} with {len(top_items)} items.")
            update_last_notified(user_id)
            save_curation_pool(user_id, sorted_pool[args.max :])
            log_digest_attempt(user_id, top_items, mode="real", status="executed")

        if args.save_html:
            save_digest_html(user_id, html, email_safe=args.email_safe)


if __name__ == "__main__":
    main()
