import sys
import os
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.youtube_fetcher import (
    fetch_new_videos,
    save_seen_video_ids,
    load_seen_video_ids,
)
from modules.transcript_fetcher import fetch_transcript
from modules.summarizer import summarize_text, log_summary
from modules.skip_cache import add_to_skipped
from modules.digest_utils import add_to_digest
from modules.user_digest import add_to_user_digest
from agents.email_agent import send_email
from modules.user_profile import load_user_profiles, load_user_profile
from modules.smart_scorer import smart_score_summary

CONFIG_PATH = "control_plane/config.yaml"
MAX_VIDEOS = 5  # Temporary limit for development/testing
DIGEST_LOWER_THRESHOLD = 0.3


def run_pipeline():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    youtube_sources = config.get("sources", {}).get("youtube", [])
    new_videos = fetch_new_videos(youtube_sources)[:MAX_VIDEOS]
    seen_ids = load_seen_video_ids()

    if not new_videos:
        print("✅ No new videos found.")
        return

    print(f"🔍 Found {len(new_videos)} new video(s). Processing...")

    user_profiles = load_user_profiles()

    for video in new_videos:
        print(f"\n🎥 {video['title']} ({video['channel']})")
        print(f"🔗 {video['url']}")

        transcript = fetch_transcript(video["video_id"])
        if not transcript:
            print("⚠️ Skipping due to missing transcript.")
            add_to_skipped(
                video_id=video["video_id"],
                title=video["title"],
                url=video["url"],
                channel=video["channel"],
            )
            continue

        summary = summarize_text(transcript)
        if not summary:
            print("⚠️ Summarization failed. Skipping.")
            continue

        for profile in user_profiles:
            score = smart_score_summary(summary, profile)
            print(f"📈 Score for {profile['user_id']}: {score}")

            log_summary(video, summary, score)

            if score >= profile.get("notification_threshold", 0.5):
                print("📧 Sending alert...")
                email_subject = f"🔥 Tech Alert: {video['title']}"
                email_body = f"Channel: {video['channel']}\nTitle: {video['title']}\nLink: {video['url']}\n\nSummary:\n{summary}"
                send_email(email_subject, email_body, to=profile["email"])

            elif score >= profile.get("digest_threshold", DIGEST_LOWER_THRESHOLD):
                print("📥 Added to user digest queue.")
                add_to_user_digest(
                    profile["user_id"],
                    {
                        "title": video["title"],
                        "channel": video["channel"],
                        "url": video["url"],
                        "summary": summary,
                    },
                )
            else:
                print("🚫 Did not meet relevance threshold. Skipping notification.")

        seen_ids.add(video["video_id"])

    save_seen_video_ids(seen_ids)


def run_pipeline_for_user(user_id, profile):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    youtube_sources = config.get("sources", {}).get("youtube", [])
    new_videos = fetch_new_videos(youtube_sources)[:MAX_VIDEOS]
    seen_ids = load_seen_video_ids()

    if not new_videos:
        print("✅ No new videos found.")
        return

    print(f"🔍 Found {len(new_videos)} new video(s). Processing...")

    for video in new_videos:
        print(f"\n🎥 {video['title']} ({video['channel']})")
        print(f"🔗 {video['url']}")

        transcript = fetch_transcript(video["video_id"])
        if not transcript:
            print("⚠️ Skipping due to missing transcript.")
            add_to_skipped(
                video_id=video["video_id"],
                title=video["title"],
                url=video["url"],
                channel=video["channel"],
            )
            continue

        # 🆕 NEW: Skip scoring if user follows the channel
        channel_followed = video["channel"] in profile.get("interests", {}).get(
            "preferred_channels", []
        )
        if channel_followed:
            print(
                "\U0001f3af User follows this channel. Adding to digest instead of immediate alert."
            )
            add_to_user_digest(
                user_id,
                {
                    "title": video["title"],
                    "channel": video["channel"],
                    "url": video["url"],
                    "summary": "This video is from a channel you follow.",
                    "source": "direct",
                },
            )
            seen_ids.add(video["video_id"])
            continue

        summary = summarize_text(transcript)
        if not summary:
            print("⚠️ Summarization failed. Skipping.")
            continue

        score = smart_score_summary(summary, profile)
        print(f"📈 Score for {user_id}: {score}")

        log_summary(video, summary, score)

        if score >= profile.get("notification_threshold", 0.5):
            print("📧 Sending alert...")
            email_subject = f"🔥 Tech Alert: {video['title']}"
            email_body = f"Channel: {video['channel']}\nTitle: {video['title']}\nLink: {video['url']}\n\nSummary:\n{summary}"
            send_email(email_subject, email_body, to=profile["email"])

        elif score >= profile.get("digest_threshold", DIGEST_LOWER_THRESHOLD):
            print("📥 Added to user digest queue.")
            add_to_user_digest(
                user_id,
                {
                    "title": video["title"],
                    "channel": video["channel"],
                    "url": video["url"],
                    "summary": summary,
                },
            )
        else:
            print("🚫 Did not meet relevance threshold. Skipping notification.")

        seen_ids.add(video["video_id"])

    save_seen_video_ids(seen_ids)
