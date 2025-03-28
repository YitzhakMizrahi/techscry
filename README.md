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
- ✅ Log summaries to enable auditability

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
│   ├── seen_videos.json
│   ├── skipped_videos.json
│   ├── digest_queue.json
│   └── summary_log.jsonl
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
OPENAI_API_KEY=your_openai_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
TO_EMAIL=your_email@gmail.com
MODEL_CHUNK=gpt-3.5-turbo
MODEL_MERGE=gpt-3.5-turbo
MAX_TOKENS_FOR_SAFE_SUMMARY=30000
```

And update `control_plane/config.yaml` with your desired YouTube feeds.

In `orchestrator.py`, you can control:

- `MAX_VIDEOS` – how many new videos to process per run
- `RELEVANCE_THRESHOLD` – cutoff score for triggering notification
- `DIGEST_LOWER_THRESHOLD` – minimum score to be considered for digest

---

## 🛠 Current System Behavior

- ✅ Videos with no transcript are logged in `skipped_videos.json`
- ✅ Processed videos are tracked in `seen_videos.json`
- ✅ Only videos fully processed get marked as seen
- ✅ Videos scoring between thresholds are added to `digest_queue.json`
- ✅ Digest emails include skipped video section
- ✅ All summaries + scores are logged in `summary_log.jsonl`

---

## 🔮 Future Enhancements

| Category          | Enhancement Ideas                                   |
| ----------------- | --------------------------------------------------- |
| **Scoring**       | Add LLM-based scorer alongside keywords             |
| **Agents**        | Add Telegram, Discord, Slack, webhook agents        |
| **Source Feeds**  | Add RSS, Twitter, newsletters, blogs                |
| **Observability** | Logging, error tracking, dashboard (Streamlit?)     |
| **UI**            | Dashboard to browse and filter summaries            |
| **Profiles**      | Personalized interest modeling using embeddings     |
| **Scheduling**    | Move from manual run to cron job or serverless loop |

---

## 🧩 Vision

This project follows **Modular Control Plane (MCP)** principles:

- Modular, testable, extensible code
- Event-driven pipelines
- Agent-based delivery and notification
- Scalable architecture with low friction for adding new sources and agents

---

## 🖼️ Diagrams & System Flow (optional)

> Placeholder for a future block diagram. Examples:
>
> - 📦 Module flow (Fetch → Transcribe → Summarize → Score → Notify)
> - 🛰️ Agent distribution model
> - 🧭 Event loop or MCP orchestration overview

We can use tools like Mermaid.js, Excalidraw, or plain image embeds later.

---

## ✅ Deployment Suggestions

### 1. Local (for Dev or Hobby Use)

- Use cron or Task Scheduler to trigger `python control_plane/orchestrator.py`
- Secrets stay in `.env`

### 2. VPS

- Host on DigitalOcean, Hetzner, or similar
- Use `systemd`, `cron`, or `supervisord` to run the agent

### 3. Serverless or Fly.io/Railway

- Move state files to S3 or Firestore
- Use serverless scheduler or cron job worker

---

## 🧠 Ready to Scale

The system is designed to easily:

- Add more sources (e.g., `rss_fetcher.py`, `x_fetcher.py`)
- Add new agents (`telegram_agent.py`, `discord_agent.py`, etc.)
- Switch scoring models
- Track history for transparency and tuning

> Have fun filtering the noise and amplifying what matters. TechScry is just getting started 🚀
