# orchestrator.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.youtube_fetcher import (
    fetch_new_videos,
    save_seen_video_ids,
    load_seen_video_ids,
)
from modules.transcript_fetcher import fetch_transcript
from modules.summarizer import summarize_text
from modules.scorer import score_summary, RELEVANCE_THRESHOLD
from agents.email_agent import send_email
from modules.skip_cache import add_to_skipped

CONFIG_PATH = "control_plane/config.yaml"
import yaml

MAX_VIDEOS = 5  # Temporary limit for development/testing


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

        score = score_summary(summary)
        print(f"📈 Relevance Score: {score}")

        if score >= RELEVANCE_THRESHOLD:
            print("📝 Summary:")
            print(summary)
            print("✅ Passed relevance threshold.")

            email_subject = f"🔥 Tech Alert: {video['title']}"
            email_body = f"Channel: {video['channel']}\nTitle: {video['title']}\nLink: {video['url']}\n\nSummary:\n{summary}"
            send_email(email_subject, email_body)
        else:
            print("🚫 Did not meet relevance threshold. Skipping notification.")

        # ✅ Mark as seen only after full processing
        seen_ids.add(video["video_id"])

    save_seen_video_ids(seen_ids)


if __name__ == "__main__":
    run_pipeline()
