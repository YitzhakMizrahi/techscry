# 📒 DEVLOG.md

A chronological log of major development milestones, changes, and decisions in TechScry.

---

## 🏁 Project Kickoff

**Date**: March 27, 2025

- ✅ Setup initial project scaffold
- ✅ RSS scraping for YouTube videos
- ✅ Transcript fetching and summarization with OpenAI

---

## 📬 Digest & Email System

**Date**: March 28–30, 2025

- ✅ Designed HTML email digest templates
- ✅ Implemented `send_digest.py` with preview and mock flags
- ✅ SMTP email agent configured via `.env`
- ✅ Global digest/delivery system with mock/test support

---

## 🧠 Smart Scoring + Profiles

**Date**: March 30, 2025

- ✅ `smart_scorer.py`: LLM-based scoring using GPT
- ✅ Scoring prompt includes user profile context (interests, channels)
- ✅ `user_profile.py`: JSON-based per-user interests and notification settings
- ✅ Added multi-user support via `run_pipeline.py`

---

## 🔁 Seen/Skipped/Digest Per User

**Date**: March 31, 2025

- ✅ Moved `seen_videos.json`, `skipped.json`, and `digest_queue.json` under `users/<user_id>/`
- ✅ Created per-user directories with isolated state
- ✅ Updated all logic to use user-based state paths

---

## 🗓️ Curated Digest & Notification Gate

**Date**: March 31, 2025

- ✅ `send_curated_digest.py` introduced (user-based curated queue)
- ✅ Notification cooldown logic added via `notification_gate.py`
- ✅ Followed channels now go to digest instead of instant alert

---

## 🧠 Summary Caching

**Date**: April 1, 2025

- ✅ `summary_cache.py` implemented
- ✅ Skips LLM if summary already exists in cache
- ✅ Cache stored in `data/summary_cache.json`
- ✅ Global summary log continues in `summary_log.jsonl`

---

## 🧪 Improved Dev Experience

**Date**: April 1, 2025

- ✅ `tests/mock/` structure for digest/skipped previewing
- ✅ Flags for `--mock`, `--preview`, `--email-safe`
- ✅ Mock digest data used for email styling/dev testing
- ✅ README.md rewritten to reflect current architecture and future plans

---

## 📦 Internal Refactoring & Cleanup

**Date**: April 1, 2025

- ✅ Archived legacy `scorer.py` (replaced by smart scoring)
- ✅ Moved mock files into `tests/`
- ✅ Modularized summary logic, transcript skipping, and smart scoring
- ✅ Structured `scripts/` directory for CLI entrypoints

---

## 🧘 Looping + Observability Added

**Date**: April 1, 2025

- ✅ `loop_runner.py` added for repeat execution with interval control
- ✅ Introduced `--dry-run` for `run_pipeline.py`
- ✅ Introduced `--log-only` and `--save-html` for `send_curated_digest.py`
- ✅ Created `logs/pipeline_log.jsonl` for system-wide event logging
- ✅ .gitignore updated to exclude data, logs, digests, and user state

---

## 🔍 Transcript Caching Validation & Cleanup

**Date**: April 3, 2025

- ✅ `transcript_cache.py` created to cache transcripts under `data/transcript_cache.json`
- ✅ `transcript_fetcher.py` patched to use cache hits before triggering fetch
- ✅ Tested repeated runs with cleared `seen_videos` to confirm skip behavior
- ✅ Added logging for cache hit/miss and summarization skipping
- ✅ Verified faster runs and no redundant LLM calls
- ✅ Removed experimental `utils/runtime.py` enforcement system (no longer needed)

---

## 🧙 Frontend Redesign & Digest Feed Polish

**Date**: April 4–6, 2025

- ✅ `create-next-app` scaffolded with Tailwind, App Router, and shadcn/ui
- ✅ Built `DigestPreview` and `SkippedVideos` components
- ✅ Added responsive grid layout, score badges, thumbnails
- ✅ Introduced YouTube modal playback with ESC to close
- ✅ Used real-world sample data to test UI under load
- ✅ Structured mock data under `/mock/`, decoupled from preview-only logic
- ✅ UI polish: typography, spacing, transitions, hover play icon, blur effect
- ✅ Began refactoring `UserAdminPanel` and debug tools
- ✅ Created `RISK_RADAR.md` to clarify priorities and prevent overbuilding

_To be continued..._
