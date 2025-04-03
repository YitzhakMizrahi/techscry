👋 Hi partner — I'm migrating our ongoing TechScry project to a new thread.

Please assume the following context and load it into memory:

---

## 🧠 TechScry — Project Overview

TechScry is an intelligent content monitoring and delivery tool that:

- 📡 Fetches YouTube videos via RSS from followed and trending channels
- 📝 Transcribes and summarizes them using OpenAI GPT models
- 📊 Scores content per user using profile-aware prompts
- 📥 Curates high-score items into per-user digest queues
- 📧 Sends digest emails based on cooldowns and thresholds
- 🧪 Supports dev/test via dry-run, preview, and mock data modes
- 📁 Stores all state in flat JSON files (no database needed)

The backend is modular, multi-user, and designed for local-first operation.

---

## 🔧 Project Status at Migration (April 3, 2025)

We’ve just completed a major backend refactor:

- ✅ Transcript + summary caching (via `transcript_cache.py` and `summary_cache.py`)
- ✅ Modular LLM summarization + relevance scoring via GPT
- ✅ Digest delivery with preview, save, and cooldown support
- ✅ Background-safe looping via `loop_runner.py`
- ✅ Per-user isolated state: `seen_videos`, `skipped.json`, `digest_queue.json`
- ✅ System event logging in `logs/pipeline_log.jsonl`
- ✅ Internal structure cleanup and updated documentation

All of this is production-ready and working reliably across two users.

---

## 🌱 What I’d Like You To Do Now

We’re about to begin the **Frontend Phase** of TechScry.

Please:

- Rebuild context in this thread
- Accept the updated backend as current ground truth
- Load the necessary files into the canvas
- Help design and scaffold a lightweight but clean UI (admin, user views, digest previews)

---

## 🔄 I Will Now Send You the Core Files in This Order

Please wait for me to send them one-by-one before responding:

### 🧠 Core Orchestration

1. `control_plane/orchestrator.py` — the central control loop
2. `scripts/run_pipeline.py` — CLI pipeline entrypoint

### 📹 Discovery & Processing

3. `modules/youtube_fetcher.py`
4. `modules/transcript_fetcher.py`
5. `modules/transcript_cache.py`
6. `modules/summarizer.py`
7. `modules/smart_scorer.py`

### 📥 User State & Digest Logic

8. `modules/user_digest.py`
9. `modules/user_profile.py`
10. `modules/skip_cache.py`
11. `modules/curation_pool.py`
12. `modules/summary_cache.py`

### 📬 Emailing & Notification Logic

13. `scripts/send_curated_digest.py`
14. `agents/email_agent.py`
15. `utils/notification_gate.py`

### 🧰 Utilities & Observability

16. `utils/logger.py`
17. `loop_runner.py`
18. `.env.template`

### 🧪 Templates & Examples

19. `templates/digest_email.html`
20. `templates/digest_email_safe.html`
21. `users/default/profile.json` — example profile
22. `config/interest_profile.json` — seed data

### 📚 Documentation

23. `docs/README.md`
24. `docs/DEVLOG.md`
25. `docs/DECISIONS.md`
26. `docs/ROADMAP.md`

---

## 🧠 Future Direction (Short-Term)

We're considering these enhancements:

- 📤 Frontend for admin metrics, user queue previews, and digest management
- 📑 Digest history view per user (local JSON inspection)
- 🧠 Dashboard to inspect logs, scores, transcript, and summaries
- ✍️ Digest feedback and user control UI
- ⚙️ Eventually: config editor (via JSON), dark mode switch, source toggles

---

Once files are loaded, I’ll rely on you to wire everything together and act like you’ve been co-piloting this project all along — helping me optimize, refactor, and evolve the system.

Let me know when you're ready and I’ll begin sending files. Let’s keep making this awesome. 🚀
