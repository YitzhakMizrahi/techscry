# logger.py
import os
import json
from datetime import datetime


def log_smart_score(
    user_id,
    video,
    summary,
    score,
    smart_used=True,
    matched_keywords=None,
):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "video_title": video["title"],
        "video_url": video["url"],
        "channel": video["channel"],
        "summary": summary,
        "score": score,
        "smart_scoring": smart_used,
    }
    if matched_keywords is not None:
        log_entry["matched_keywords"] = matched_keywords

    log_path = os.path.join("users", user_id, "scoring_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # Test sample usage
    video = {
        "title": "Why OpenAI is betting big on agents",
        "url": "https://youtube.com/watch?v=xyz123",
        "channel": "Fireship",
    }
    summary = "OpenAI just released an agent SDK that radically simplifies autonomous AI workflows."
    log_smart_score("default", video, summary, 0.85)
