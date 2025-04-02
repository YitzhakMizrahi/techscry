# modules/transcript_fetcher.py (patched to use transcript_cache)

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from modules.transcript_cache import load_cached_transcript, save_transcript_to_cache


def fetch_transcript(video_id):
    cached = load_cached_transcript(video_id)
    if cached:
        print(f"✅ Transcript cache hit for {video_id}. Skipping fetch.")
        return cached

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["en", "en-US"])
        lines = transcript.fetch()
        text = " ".join([line["text"] for line in lines])
        save_transcript_to_cache(video_id, text)
        return text
    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"❌ Transcript disabled for video: {video_id}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected transcript error for {video_id}: {e}")
        return None


if __name__ == "__main__":
    vid = "abc123"
    print(fetch_transcript(vid))
