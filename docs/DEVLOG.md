# 📒 DEVLOG.md

A chronological log of major development milestones, changes, and decisions in TechScry.

---

## 🏁 Project Kickoff

**Date**: March 27, 2025

- ✅ Setup initial project scaffold
- ✅ RSS scraping for YouTube videos
- ✅ Transcript fetching and summarization with OpenAI

---

## 📬 Digest & Email System (March 28 - 31)

- ✅ Designed HTML email digest templates
- ✅ Implemented `send_digest.py` with preview and mock flags
- ✅ SMTP email agent configured via `.env`
- ✅ Global digest/delivery system with mock/test support

---

## 🧠 Smart Scoring + Profiles

- ✅ `smart_scorer.py`: LLM-based scoring using GPT
- ✅ Scoring prompt includes user profile context (interests, channels)
- ✅ `user_profile.py`: JSON-based per-user interests and notification settings
- ✅ Added multi-user support via `run_for_all_users.py`

---

## 🔁 Seen/Skipped/Digest Per User

**Refactor Date**: April 1–2, 2025

- ✅ Moved `seen_videos.json`, `skipped_videos.json`, and `digest_queue.json` under `users/<user_id>/`
- ✅ Created per-user directories with isolated state
- ✅ Updated all logic to use user-based state paths

---

## 📥 Curated Digest & Notification Gate

- ✅ `send_curated_digest.py` introduced (user-based curated queue)
- ✅ Notification cooldown logic added via `notification_gate.py`
- ✅ Followed channels now go to digest instead of instant alert

---

## 🧠 Summary Caching

**Date**: April 3, 2025

- ✅ `summary_cache.py` implemented
- ✅ Skips LLM if summary already exists in cache
- ✅ Cache stored in `data/summary_cache.json`
- ✅ Global summary log continues in `summary_log.jsonl`

---

## 🧪 Improved Dev Experience

- ✅ `tests/mock/` structure for digest/skipped previewing
- ✅ Flags for `--mock`, `--preview`, `--email-safe`
- ✅ Mock digest data used for email styling/dev testing
- ✅ README.md rewritten to reflect current architecture and future plans

---

## 📦 Internal Refactoring & Cleanup

- ✅ Archived legacy `scorer.py` (replaced by smart scoring)
- ✅ Moved mock files into `tests/`
- ✅ Modularized summary logic, transcript skipping, and smart scoring
- ✅ Structured `scripts/` directory for CLI entrypoints

---

## 📘 Docs System Initiated

**Date**: April 4, 2025

- ✅ Added `docs/DEVLOG.md` (you are here)
- ⏳ `docs/ROADMAP.md` and `docs/DECISIONS.md` in progress

---

To be continued...
