# utils/logger.py

import os
import json
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = "logs"
PIPELINE_LOG_PATH = os.path.join(LOG_DIR, "pipeline_log.jsonl")


def log_smart_score(user_id, video, score, summary):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user_id,
        "video_id": video["video_id"],
        "title": video["title"],
        "channel": video["channel"],
        "score": score,
        "summary": summary,
    }
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join("users", user_id, "scoring_log.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def log_summary(video, summary, score):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "video_id": video["video_id"],
        "title": video["title"],
        "channel": video["channel"],
        "url": video["url"],
        "summary": summary,
        "score": score,
    }
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open("data/summary_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_pipeline_event(user_id, action, mode, status, items=None, cooldown_active=None):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user_id,
        "action": action,
        "mode": mode,
        "status": status,
    }
    if items is not None:
        entry["items"] = items
    if cooldown_active is not None:
        entry["cooldown_active"] = cooldown_active

    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(PIPELINE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
