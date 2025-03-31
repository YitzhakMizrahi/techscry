# 🧠 TechScry

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

TechScry monitors AI/tech YouTube channels, summarizes videos using OpenAI, scores their relevance for each user, and delivers curated digests via email.

---

## 🚀 Features

- 🔎 **Video Discovery**: Pulls from RSS feeds of followed and trending channels
- 🗘 **Transcription & Summarization**: OpenAI-based LLM summaries with chunk merging
- 📊 **Smart Scoring**: Personalized GPT scoring based on per-user interests
- 🛅 **Curation Pool**: Per-user prioritized digest queues with timestamps
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
├── archive/                 # Deprecated modules
├── config/                  # Interest profile seed
├── control_plane/          # Orchestration logic
├── data/                   # Shared cache (summaries)
├── digests/                # Saved email HTML output
├── docs/                   # Docs: DEVLOG, ROADMAP, DECISIONS
├── modules/                # Core logic modules
├── scripts/                # CLI entrypoints (digest, pipeline)
├── templates/              # Jinja HTML email templates
├── tests/mock/             # Preview/test fixtures
├── users/                  # Per-user state & preferences
├── utils/                  # Utilities (logger, cooldown, chunking)
├── loop_runner.py          # Universal interval-based loop executor
├── .env.template           # Configuration template
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

Use `loop_runner.py` to schedule:

```bash
python loop_runner.py --script scripts/run_pipeline.py --args --dry-run --interval 900
python loop_runner.py --script scripts/send_curated_digest.py --args --log-only --interval 900
```

---

## 🗃️ Logs

Logs stored in `logs/pipeline_log.jsonl` track each user's:

- Digest dispatch
- Pipeline runs
- Dry run/testing status

---

## 🧩 Design Principles

- **Context-Aware Delivery**: Respects user preferences, follows cooldowns
- **Minimal LLM Cost**: Caching, chunking, and relevance filtering built-in
- **Scalable via JSON**: Fully user-isolated—no DB or server required
- **Human-Friendly Previews**: Digest HTML + mock data for local design testing

---

## 🌱 Want More?

Check the `docs/` folder for:

- `DEVLOG.md` — Historical change tracking
- `DECISIONS.md` — Design choices
- `ROADMAP.md` — Vision and next steps

---

Built with ❤️ by TechScry Labs
