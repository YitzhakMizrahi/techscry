# 📜 DECISIONS.md

A log of important architectural and design decisions made throughout the TechScry project.

---

## ✅ Core Philosophy

- **Digest-first, non-intrusive**: Deliver content summaries in batches instead of flooding the user with real-time alerts.
- **LLM-Powered Relevance**: Leverage GPT scoring to personalize video relevance for each user.
- **No DB, JSON-first**: Stick with per-user JSON files until the system requires something more scalable.
- **Per-user State Isolation**: Each user has their own digest queue, seen videos, skipped list, and preferences.

---

## 🔍 Data & Caching

- **`summary_cache.json`**: Global cache to deduplicate summaries and avoid unnecessary LLM calls.
- **`summary_log.jsonl`**: Keeps a full log of all summaries and their scores for analysis and debugging.

---

## 🔄 Notification Logic

- **Cooldown logic** lives in `notification_gate.py`, with optional overrides from user settings.
- **Followed Channels** are treated differently:
  - Originally: Instant alert
  - Now: Queued in digest for uniform delivery UX

---

## 🧪 Testing Philosophy

- We use mock data under `tests/mock/` to preview emails and iterate quickly.
- `--mock`, `--preview`, `--email-safe` flags exist to simulate production behavior safely.

---

## 🔗 Channel Sourcing

- We aggregate all YouTube RSS feeds from user profiles instead of maintaining a global static list.
- `channel_pool.py` handles this aggregation.

---

## 🛠️ Tooling

- LLM model selection is configurable via `.env`
- Core logic is broken into `modules/`, orchestration lives in `control_plane/`
- Scripts go into `scripts/` and follow CLI-friendly structure

---

## ⌛ Upcoming Considerations

- When to move to a database (thresholds TBD)
- When to introduce background jobs / workers
- When to integrate external notification channels (Telegram, WhatsApp, etc)

---

_Last updated: [March 30, 2025]_
