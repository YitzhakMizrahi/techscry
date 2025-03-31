# 🗺️ TechScry Roadmap

A living roadmap outlining active priorities, near-term upgrades, and long-term vision for TechScry.

---

## ✅ Recently Completed (March–April 1, 2025)

- 🔧 Refactored to fully support per-user state (seen/skipped/digest → curation_pool)
- 🧠 Smart scoring with GPT using profile-aware prompt
- 🛅 Digest queue split from real-time delivery (cooldown-aware)
- 📥 Curated email digest with dark/light templates and skipped-video fallback
- 🧪 Mock data system + preview/testing CLI flags (`--mock`, `--preview`, `--email-safe`, `--log-only`)
- ⚙️ Summary cache system using `summary_cache.json` to prevent duplicate LLM calls
- 🧭 `run_pipeline.py` and `send_curated_digest.py` now support:
  - `--dry-run`
  - Logging to `logs/pipeline_log.jsonl`
  - Time-based `loop_runner.py` for background scheduling
- 🛠️ `.gitignore`, `.gitattributes`, and file hygiene cleanup

---

## 🧩 In Progress

- 🛑 Settled Mode for Onboarding:
  - Users in "catching_up" mode skip real-time alerts
  - Transitions to "settled" after seen queue stabilizes
- 🛠 `state.json` file per user to track digest state
- 📡 Expanded YouTube source list for more discovery

---

## 🔜 Near-Term Priorities

- 🧵 Replace `MAX_VIDEOS` with config or CLI flag
- 🛠 Allow `digest_threshold` to influence scoring decisions
- 📨 Create `digest_runner.py` that respects per-user cooldown timers for delivery
- 👥 Multi-user mock data generator
- 💬 Digest email footer with opt-out / feedback link

---

## 🌐 Long-Term Vision

- 🌍 Expand beyond YouTube (e.g., Arxiv, Hacker News, X)
- 💬 Slack / Discord bot for delivery (configurable)
- 📊 Admin dashboard for metrics and queue visibility
- 🧠 LLM fallback or hybrid scoring (keyword + GPT)
- ⚙️ Move to a background job system (e.g., APScheduler, RedisQueue)
- 📦 Optional SQLite or light DB backend
- 🧪 Test suite (unit + integration + fixtures)
- 🚀 Docker + PM2/cron + cloud deploy script
- 🧱 Web UI for config editing and digest review

---

_Last updated: April 1, 2025_

Built with ❤️ by TechScry Labs
