import json
from pathlib import Path

SUMMARY_CACHE_PATH = "data/summary_cache.json"


def _load_cache():
    if not Path(SUMMARY_CACHE_PATH).exists():
        return {}
    with open(SUMMARY_CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_cache(cache):
    Path(SUMMARY_CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_summary(video_id: str) -> str | None:
    cache = _load_cache()
    return cache.get(video_id)


def save_summary(video_id: str, summary: str) -> None:
    cache = _load_cache()
    cache[video_id] = summary
    _save_cache(cache)


def summary_exists(video_id: str) -> bool:
    cache = _load_cache()
    return video_id in cache


if __name__ == "__main__":
    test_id = "abc123"
    test_summary = "This is a summary of a test video."
    save_summary(test_id, test_summary)
    print("Exists:", summary_exists(test_id))
    print("Summary:", get_summary(test_id))
