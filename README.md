# 🧠 TechScry – AI-Powered Tech Signal Filter

TechScry is a modular, event-driven tool that listens to cutting-edge YouTube channels, summarizes new content, scores it for relevance, and notifies you only when it's noteworthy.

---

## 🚀 MVP Goal (Phase 1)

- ✅ Fetch new videos from a list of curated YouTube channels
- ✅ Retrieve transcripts (if available)
- ✅ Summarize transcript using LLM (OpenAI API)
- ✅ Score the content’s relevance (via keywords or AI)
- ✅ Notify via email if score > threshold
- ✅ Queue mid-interest content for digest
- ✅ Track skipped videos and include them in digest reports
- ✅ Store summary logs for later insights/debugging

---

## 📁 Project Structure (MCP-style)

```bash
techscry/
├── control_plane/       # Orchestration logic
│   ├── orchestrator.py
│   ├── config.yaml
│   └── cli.py
├── modules/             # Modular functional units
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── scorer.py
│   ├── skip_cache.py
│   └── digest_utils.py
├── agents/              # Delivery agents (email, CLI, etc.)
│   ├── email_agent.py
│   └── cli_logger.py (planned)
├── data/                # Local cache and state
│   ├── seen_videos.json
│   ├── skipped_videos.json
│   ├── digest_queue.json
│   └── summary_log.jsonl
├── utils/               # Helpers like chunking, formatting
│   └── chunking.py
├── scripts/             # Standalone helpers
│   └── skipped_report.py
├── .env                 # API keys and config
├── requirements.txt
└── README.md
```

---

## 📚 Modules Overview

| Module               | Description                                           |
| -------------------- | ----------------------------------------------------- |
| `youtube_fetcher`    | Parses RSS feeds and returns unseen, unskipped videos |
| `transcript_fetcher` | Gets transcript via `youtube-transcript-api`          |
| `summarizer`         | Summarizes transcript using GPT                       |
| `scorer`             | Scores summary relevance using keywords               |
| `skip_cache`         | Tracks unprocessable videos (e.g. no transcript)      |
| `digest_utils`       | Stores mid-interest content and formats digest email  |
| `email_agent`        | Sends emails using SMTP credentials                   |

---

## ⚙️ Configuration

Set your `.env` like:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
TO_EMAIL=your_email@gmail.com
OPENAI_API_KEY=your_openai_key
MODEL_CHUNK=gpt-3.5-turbo
MODEL_MERGE=gpt-3.5-turbo
MAX_TOKENS_FOR_SAFE_SUMMARY=30000
```

Update `control_plane/config.yaml` with your desired YouTube feeds.

---

## 🛠 Current System Behavior

- ✅ Videos with no transcript are logged in `skipped_videos.json`
- ✅ Processed videos are tracked in `seen_videos.json`
- ✅ Only videos fully processed get marked as seen
- ✅ Videos scoring between 0.3 and 0.49 are added to the digest queue
- ✅ Digest email includes digest-worthy videos and skipped titles (with links)
- ✅ Summaries and scores are stored in `summary_log.jsonl`

---

## 🔧 CLI Utilities

| Script              | Function                                         |
| ------------------- | ------------------------------------------------ |
| `orchestrator.py`   | Runs the full fetch → summarize → score pipeline |
| `send_digest.py`    | Sends out the digest email                       |
| `skipped_report.py` | Shows skipped videos from cache                  |
| `cli.py` (future)   | Unified CLI for all above                        |

---

## 🧠 Vision

This project follows **Modular Control Plane (MCP)** principles:

- Modular design
- Event-driven
- Agent-based delivery
- Policy/scoring-driven filtering

With long-term goals to:

- Support multi-agent delivery (Telegram, browser, etc.)
- Expand beyond YouTube (RSS, podcasts, newsletters)
- Enable custom profiles + web UI for personalized digests

---

## 🚨 Ideas + Backlog

| Area             | Idea                                                    |
| ---------------- | ------------------------------------------------------- |
| Email Design     | Upgrade digest formatting to rich HTML                  |
| Scheduling       | Add cron-based or persistent orchestrator               |
| Fallback         | Whisper/audio fallback for transcript-less videos       |
| AI Scoring       | Add relevance scoring via GPT + user interest vectors   |
| Source Expansion | Add support for RSS feeds, blogs, Twitter               |
| Profile Support  | Prepare config system for multi-user personalization    |
| Observability    | Debug logs, run history, optional dashboard (Streamlit) |

---

## 🚀 Deployment Paths

| Method         | Pros                           | Setup Level |
| -------------- | ------------------------------ | ----------- |
| Local Runner   | Simple, private                | 🟢 Easy     |
| VPS Cron Job   | Persistent, flexible           | 🟡 Medium   |
| Railway/Fly.io | Scalable, auto-deploys         | 🟠 Medium+  |
| Serverless     | Cost-effective, trickier state | 🔴 Advanced |

---

You're building a personal intelligence system. Keep shipping. ✨
