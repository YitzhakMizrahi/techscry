# modules/transcript_fetcher.py (final fix for snippet handling)

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

        # Normalize all transcript lines to string safely
        text_lines = []
        for line in lines:
            try:
                text_lines.append(line["text"])  # dict case
            except (TypeError, KeyError):
                try:
                    text_lines.append(line.text)  # object case
                except Exception:
                    text_lines.append(str(line))  # fallback to string

        text = " ".join(text_lines)
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
