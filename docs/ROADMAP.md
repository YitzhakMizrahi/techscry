# 🗺️ TechScry Roadmap

A living roadmap that outlines current priorities, short-term goals, and long-term aspirations for TechScry.

---

## ✅ Recently Completed

- 🔧 Refactored to fully support per-user state (seen/skipped/digest)
- 🧠 Implemented global summary cache (`summary_cache.json`) to reduce LLM calls
- 📬 Introduced curated digest queuing with cooldown support
- 🛠️ Migrated to `scripts/` CLI interface with flags (`--preview`, `--mock`, etc.)
- 🧪 Improved test/dev tooling with mock data and structured directories

---

## 🧩 In Progress

- 📧 Finalize curated digest delivery flow (top-N from queue)
- 🧼 Polish digest email rendering (mobile-responsive, fallback messages)
- ⚙️ Add configurable user flags (e.g., real-time alerts, digest-only)
- 🧪 Extend `run_pipeline.py` with `--mock` and `--user` flags
- 📝 Clean up unused imports and deprecated code

---

## 🧭 Near-Term

- 🔁 Implement loop/cron-style execution with smart cooldown checks
- 🧠 Improve scoring heuristics by combining keyword match + LLM score
- 🔐 Add support for secure user onboarding via config or CLI
- 🧵 Split global config into environment vs user-facing pieces
- 📥 Create tools to inspect and filter digests before sending

---

## 🌐 Long-Term Vision

- 🌍 Expand beyond YouTube (e.g., Twitter/X, Arxiv, Hacker News)
- 💬 Add Telegram or Discord bot integration for digest delivery
- 📊 Admin dashboard for managing users, logs, and queues
- 🤖 Train a lightweight local model to replace scoring LLMs
- 📦 Optional migration to SQLite or lightweight DB backend
- 🌈 UX polish: interactive web-based digest viewer / reader

---

_Last updated: March 30, 2025_

Built with ❤️ by TechScry Labs
