# 🔠 TechScry

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

TechScry monitors AI/tech YouTube channels, summarizes videos using OpenAI, scores their relevance for each user, and delivers curated digests via email.

---

## 🚀 Features

- 🔎 **Video Discovery**: Pulls from RSS feeds of followed and trending channels
- 🗘️ **Transcription & Summarization**: OpenAI-based LLM summaries with chunk merging
- 📊 **Smart Scoring**: Personalized GPT scoring based on per-user interests
- 🗕 **Curation Pool**: Per-user prioritized digest queues with timestamps
- 🧠 **Summary Caching**: Avoids redundant LLM calls via summary deduplication
- 📧 **Digest Delivery**: Styled emails with cooldown-aware delivery logic
- 🧪 **Mocking & Previews**: Dry runs, preview flags, HTML saves for dev & testing
- 🧵 **Multi-user Support**: Fully isolated state per user (seen, skipped, scores)
- 🔁 **Script Looping**: Background-ready with `loop_runner.py`
- 📄 **System Logging**: Output to `logs/pipeline_log.jsonl` for visibility

---

## 🏠 Project Structure

```bash
techscry/
├── agents/                  # Email agent (SMTP)
│   └── email_agent.py
├── archive/                 # Deprecated modules
│   └── scorer.py
├── config/                  # Interest profile seed
│   └── interest_profile.json
├── control_plane/           # Orchestration logic
│   └── orchestrator.py
├── data/                    # Shared cache (summaries)
│   └── summary_cache.json
├── digests/                 # Saved email HTML output
├── docs/                    # Docs: DEVLOG, ROADMAP, DECISIONS
│   ├── DEVLOG.md
│   ├── ROADMAP.md
│   └── DECISIONS.md
├── frontend/                 # 📌 New: Next.js-based feed viewer
├── modules/                 # Core logic modules
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── transcript_cache.py
│   ├── user_profile.py
│   ├── skip_cache.py
│   └── curation_pool.py
├── scripts/                 # CLI entrypoints (digest, pipeline)
│   ├── run_pipeline.py
│   ├── send_curated_digest.py
│   └── dev_send_digest.py
├── templates/               # Jinja HTML email templates
│   ├── digest_email.html
│   └── digest_email_safe.html
├── tests/mock/              # Preview/test fixtures
│   ├── mock_digest_data.json
│   └── mock_skipped_videos.json
├── users/                   # Per-user state & preferences
│   └── <user_id>/
│       ├── profile.json
│       ├── seen_videos.json
│       ├── skipped.json
│       └── digest_queue.json
├── utils/                   # Utilities (logger, cooldown, chunking)
│   ├── logger.py
│   ├── chunking.py
│   └── notification_gate.py
├── loop_runner.py           # Universal interval-based loop executor
├── .env.template            # Configuration template
└── requirements.txt
```

---

## 🔧 Setup

```bash
git clone https://github.com/YitzhakMizrahi/techscry.git
cd techscry
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.template .env
```

Then edit `.env` with your own API and SMTP credentials.

---

## 👤 Add Users

Create a profile like this:

```json
// users/<id>/profile.json
{
  "email": "user@example.com",
  "interests": {
    "keywords": ["gpt", "react", "openai"],
    "preferred_channels": ["Fireship"]
  },
  "notification_settings": {
    "notification_threshold": 0.6,
    "digest_threshold": 0.3,
    "max_per_digest": 5,
    "cooldown_hours": 12
  }
}
```

---

## 🧪 Development Flags

| Flag           | Script                   | Description                      |
| -------------- | ------------------------ | -------------------------------- |
| `--dry-run`    | `run_pipeline.py`        | Simulates pipeline, logs actions |
| `--verbose`    | `run_pipeline.py`        | Print full debug output          |
| `--preview`    | `send_curated_digest.py` | Open rendered HTML in browser    |
| `--log-only`   | `send_curated_digest.py` | Simulate sending, log only       |
| `--save-html`  | `send_curated_digest.py` | Save HTML digest to `digests/`   |
| `--email-safe` | Any sender               | Use email-compatible HTML        |

---

## 🔁 Background Automation

Use `loop_runner.py` with `-m` to schedule background tasks:

```bash
# ❗ Usage Reminder
All scripts must be run using `-m` from the project root. For example:

python -m loop_runner --script scripts.run_pipeline --interval 900 --args --dry-run
python -m loop_runner --script scripts.send_curated_digest --interval 900 --args --log-only
```

---

## 📃 Logs

Logs stored in `logs/pipeline_log.jsonl` track each user's:

- Digest dispatch
- Pipeline runs
- Dry run/testing status

---

## 🌐 Frontend App (Next.js)

The `frontend/` directory contains a fully client-rendered Next.js UI for digest preview and skipped video inspection.

### ⚡ Features

- Digest cards with title, summary, relevance badge
- YouTube modal player on click
- Hover play icon for visual feedback
- Skipped video listing
- Responsive design (1–6 columns depending on screen size)

### 🧪 Dev Setup

```bash
cd frontend
pnpm install
pnpm dev
```

Visit http://localhost:3000/user/default for the default user’s feed.

---

## 🤩 Design Principles

- **Context-Aware Delivery**: Respects user preferences, follows cooldowns
- **Minimal LLM Cost**: Caching, chunking, and relevance filtering built-in
- **Scalable via JSON**: Fully user-isolated—no DB or server required
- **Human-Friendly Previews**: Digest HTML + mock data for local design testing

---

## 📚 Docs & Planning

Check the `docs/` folder for:

- [docs/DEVLOG.md](docs/DEVLOG.md) — Historical change tracking
- [docs/DECISIONS.md](docs/DECISIONS.md) — Design choices
- [docs/ROADMAP.md](docs/ROADMAP.md) — Vision and next steps
- [docs/RISK_RADAR.md](docs/RISK_RADAR.md) — Risks & mitigation

---

Built with ❤️ by TechScry Labs
