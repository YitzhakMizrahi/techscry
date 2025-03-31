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

## ↺ Notification Logic

- **Cooldown logic** lives in `notification_gate.py`, with overrides from user settings.
- **Followed Channels** behavior:
  - Originally: Immediate alerts
  - Now: Digest-first delivery for smoother onboarding

---

## 🔎 Smart Onboarding ("Settled Mode")

- **`state.json`** tracks if user is still "catching_up" or "settled"
- New users get all content in digests while catching up
- Alerts resume when user has seen enough recent videos

---

## 🚪 Skipping & Digest Queue

- Videos without transcripts go to `skipped.json` with metadata
- Digest queues managed via `curation_pool.py`, replacing `user_digest.py`
- Per-user queues prioritized by relevance score

---

## 🧩 Testing Philosophy

- Use mock data under `tests/mock/` to preview digest emails
- `--mock`, `--preview`, `--log-only`, and `--dry-run` flags simulate behavior safely

---

## 🔗 Channel Aggregation

- RSS feeds dynamically built by aggregating all `preferred_channels` from user profiles
- No static list needed (though fallback exists in `control_plane/config.yaml`)

---

## 🛠️ Tooling

- Model & SMTP config is `.env`-based
- Modular structure: `modules/`, `control_plane/`, `scripts/`
- System-wide logging enabled via `logs/pipeline_log.jsonl`

---

## ⌛ Looping & Scheduling

- Looping supported with `loop_runner.py` for both pipeline & digest dispatch
- User-level cooldown respected via config (e.g. `cooldown_hours`)

---

## ⏳ Pending Improvements

- Email opt-in preferences and frequency controls
- User onboarding via web or CLI
- Background scheduling for long-term use (cron, pm2, docker)

---

_Last updated: [April 1, 2025]_
