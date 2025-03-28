# send_digest.py

from modules.digest_utils import (
    load_digest_queue,
    format_digest_email,
    clear_digest_queue,
)
from agents.email_agent import send_email


def main():
    queue = load_digest_queue()
    if not queue:
        print("📭 Digest queue is empty. Nothing to send.")
        return

    email_subject = "🗞️ TechScry Digest"
    email_body = format_digest_email(queue)

    try:
        send_email(email_subject, email_body)
        clear_digest_queue()
        print("✅ Digest email sent and queue cleared.")
    except Exception as e:
        print(f"❌ Failed to send digest email: {e}")


if __name__ == "__main__":
    main()
