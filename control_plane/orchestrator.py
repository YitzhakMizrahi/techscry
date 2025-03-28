# orchestrator.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.youtube_fetcher import fetch_new_videos
from modules.transcript_fetcher import fetch_transcript
from modules.summarizer import summarize_text

CONFIG_PATH = "control_plane/config.yaml"
import yaml

MAX_VIDEOS = 5  # Temporary limit for development/testing


def run_pipeline():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    youtube_sources = config.get("sources", {}).get("youtube", [])
    new_videos = fetch_new_videos(youtube_sources)[:MAX_VIDEOS]

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
            continue

        summary = summarize_text(transcript)
        if not summary:
            print("⚠️ Summarization failed. Skipping.")
            continue

        print("📝 Summary:")
        print(summary)
        print("✅ Done.\n")


if __name__ == "__main__":
    run_pipeline()
