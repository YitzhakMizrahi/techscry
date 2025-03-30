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
from modules.user_digest import add_to_user_digest
from agents.email_agent import send_email
from modules.smart_scorer import smart_score_summary
from modules.channel_pool import get_all_followed_channels
from utils.logger import log_smart_score
from utils.notification_gate import is_notification_allowed, update_last_notified

CONFIG_PATH = "control_plane/config.yaml"
MAX_VIDEOS = 5  # Temporary limit for development/testing


def run_pipeline_for_user(
    user_id, profile, verbose=False, send_direct_notifications=False
):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    youtube_sources = config.get("sources", {}).get("youtube", [])
    new_videos = fetch_new_videos(youtube_sources)[:MAX_VIDEOS]
    seen_ids = load_seen_video_ids(user_id)

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

        channel_followed = video["channel"] in profile.get("interests", {}).get(
            "preferred_channels", []
        )
        if channel_followed:
            if send_direct_notifications:
                print(
                    "🎯 User follows this channel. Skipping scoring and sending direct alert."
                )
                send_email(
                    subject=f"🔔 New Video from {video['channel']}: {video['title']}",
                    html_body=(
                        f"Channel: {video['channel']}<br>"
                        f"Title: {video['title']}<br>"
                        f"Link: <a href='{video['url']}'>{video['url']}</a><br><br>"
                        f"(This video is from a channel the user follows directly.)"
                    ),
                    to=profile["email"],
                )
            else:
                print("📥 Followed channel video queued for digest.")
                add_to_user_digest(
                    user_id,
                    {
                        "title": video["title"],
                        "channel": video["channel"],
                        "url": video["url"],
                        "summary": "(This video is from a channel the user follows directly.)",
                    },
                )
            seen_ids.add(video["video_id"])
            continue

        summary = summarize_text(transcript)
        if not summary:
            print("⚠️ Summarization failed. Skipping.")
            continue

        score = smart_score_summary(summary, profile, verbose=verbose)
        if verbose:
            print(f"📈 [Smart Score] {score} for user '{user_id}' on: {video['title']}")

        print(f"📈 Score for {user_id}: {score}")

        log_smart_score(user_id=user_id, video=video, score=score, summary=summary)
        log_summary(video, summary, score)

        if score >= profile.get("notification_settings", {}).get(
            "notification_threshold", 0.5
        ):
            print("📥 Added to curated digest pool for later delivery.")
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

    save_seen_video_ids(user_id, seen_ids)
