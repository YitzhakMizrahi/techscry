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

---

## 📁 Project Structure (MCP-style)

```bash
techscry/
├── control_plane/             # Orchestrator logic
│   ├── main.py                # Entry point
│   ├── orchestrator.py        # Core logic
│   └── config.yaml            # Source list, rules, thresholds
│
├── modules/                   # Modular logic units
│   ├── youtube_fetcher.py     # Polls channels (RSS/API)
│   ├── transcript_fetcher.py  # Gets captions/transcripts
│   ├── summarizer.py          # Summarizes transcript (GPT or fallback)
│   ├── scorer.py              # Scores relevance of content
│   ├── skip_cache.py          # Tracks skipped (unprocessable) content
│   └── digest_utils.py        # Queue + format digest email content
│
├── agents/                    # Agents that execute side effects
│   ├── email_agent.py         # Sends email via SMTP
│   ├── cli_logger.py          # Prints/logs locally (planned)
│   └── telegram.py            # Future: Send message to Telegram (optional)
│
├── data/                      # Local state or cache
│   ├── seen_videos.json       # Successfully processed video IDs
│   ├── skipped_videos.json    # Permanently unprocessable (e.g. no transcript)
│   └── digest_queue.json      # Mid-score content for digest
│
├── utils/                     # Common helpers
│   └── chunking.py            # Break long text into LLM-friendly chunks
│
├── .env                       # Your keys/config (e.g., OpenAI, SMTP)
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
```

And update `control_plane/config.yaml` with your desired YouTube feeds.

In `orchestrator.py`, you can control:

- `MAX_VIDEOS` – how many new videos to process per run
- `RELEVANCE_THRESHOLD` – cutoff score for triggering notification

---

## 🛠 Current System Behavior

- ✅ Videos with no transcript are logged in `skipped_videos.json`
- ✅ Processed videos are tracked in `seen_videos.json`
- ✅ Only videos fully processed get marked as seen
- ✅ Videos scoring between 0.5 and 0.79 are added to the digest queue
- ✅ Digest email will include both digest-worthy videos and skipped titles (with links)

---

## 🗓️ Development Progress

- ✅ MVP architecture scaffolded
- ✅ Modular fetch-transcribe-summarize-score pipeline
- ✅ Relevance filtering via keyword matcher
- ✅ Email agent operational
- ✅ Smart seen/skipped caching logic in place
- ✅ Digest system scaffolded
- ✅ README updated for current structure
- 🔜 Digest email scheduler
- 🔜 Whisper fallback (optional)

---

## 🧩 Vision

This project follows **Modular Control Plane (MCP)** principles:

- Modular design
- Event-driven
- Agent-based delivery
- Policy/scoring-driven filtering
