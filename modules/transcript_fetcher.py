# transcript_fetcher.py

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item["text"] for item in transcript])
        return full_text
    except TranscriptsDisabled:
        print(f"❌ Transcript disabled for video: {video_id}")
    except NoTranscriptFound:
        print(f"⚠️ No transcript found for video: {video_id}")
    except Exception as e:
        print(f"⚠️ Error fetching transcript for {video_id}: {e}")
    return None
