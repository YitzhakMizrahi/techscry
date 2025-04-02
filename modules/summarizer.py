# summarizer.py
import os
import json
from dotenv import load_dotenv
from utils.chunking import chunk_text
from openai import OpenAI
from modules.summary_cache import summary_exists, get_summary, save_summary

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)

MODEL_CHUNK = os.getenv("MODEL_CHUNK", "gpt-3.5-turbo")
MODEL_MERGE = os.getenv("MODEL_MERGE", "gpt-3.5-turbo")
SUMMARY_LOG_PATH = "data/summary_log.jsonl"
MAX_TOKENS_FOR_SAFE_SUMMARY = int(os.getenv("MAX_TOKENS_FOR_SAFE_SUMMARY", 30000))


def summarize_chunk(chunk):
    try:
        response = client.chat.completions.create(
            model=MODEL_CHUNK,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes YouTube transcripts.",
                },
                {
                    "role": "user",
                    "content": f"Summarize this transcript chunk:\n\n{chunk}",
                },
            ],
        )
        return response.choices[0].message.content.strip()
    except KeyboardInterrupt:
        print("🛑 Interrupted during summarization. Exiting cleanly.")
        raise  # Let it bubble up for graceful exit
    except Exception as e:
        print(f"⚠️ Error during summarizing chunk: {e}")
        return None


def summarize_text(video_id, transcript):
    if video_id and summary_exists(video_id):
        print(f"✅ Summary cache hit for {video_id}. Skipping LLM call.")
        return get_summary(video_id)

    if len(transcript.split()) > MAX_TOKENS_FOR_SAFE_SUMMARY:
        print(
            f"🚫 Transcript too long ({len(transcript.split())} words). Skipping summarization."
        )
        return None

    chunks = chunk_text(transcript, max_tokens=2000)
    print(f"🧩 Transcript split into {len(chunks)} chunk(s).")

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"✂️ Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        if summary:
            summaries.append(summary)
        else:
            print(f"⚠️ Skipping chunk {i+1} due to summarization failure.")

    if not summaries:
        return None

    combined = "\n".join(summaries)
    if len(summaries) == 1:
        final_summary = summaries[0]
    else:
        print("🧠 Merging chunk summaries...")
        try:
            response = client.chat.completions.create(
                model=MODEL_MERGE,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that merges short summaries into a final one.",
                    },
                    {
                        "role": "user",
                        "content": f"Merge these into a single concise summary:\n\n{combined}",
                    },
                ],
            )
            final_summary = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ Error during merge summarization: {e}")
            final_summary = combined

    if video_id:
        save_summary(video_id, final_summary)

    return final_summary


def log_summary(video, summary, score):
    os.makedirs("data", exist_ok=True)
    log = {
        "title": video["title"],
        "channel": video["channel"],
        "url": video["url"],
        "score": score,
        "summary": summary,
    }
    with open(SUMMARY_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    with open("example_transcript.txt", "r") as f:
        text = f.read()
        print(summarize_text("example_video_id", text))
