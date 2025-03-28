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

## 🚨 Areas We Could Improve or Expand

| Category                  | Observation / Opportunity                    | Suggestion                                      |
| ------------------------- | -------------------------------------------- | ----------------------------------------------- |
| **Scoring**               | Right now, all summaries are treated equally | Add a keyword-based or AI scoring layer         |
| **Notification delivery** | Output only goes to email                    | Add more agents (and/or Telegram/SMS for later) |
| **Scheduling**            | You must run it manually                     | Add cron job or background daemon later         |
| **Transcript fallback**   | No captions = skip entirely                  | Use Whisper or audio fallback later             |
| **Observability**         | No logs or dashboard to trace actions        | Simple CLI logs now, maybe Streamlit view later |
| **Source diversity**      | Only supports YouTube                        | Add RSS feeds or Twitter in future phases       |

---

## 💡 What We’re Not Doing Yet (But Could Later)

- 📊 Dashboard or digest format (weekly summary email?)

- 🔍 Queryable summary store (e.g. search for topics you care about)

- 🧠 LLM-based “interest profile” (let the AI learn what you care about)

- 🧰 Plugin framework (e.g. plug in a new source without changing control logic)

---

## ✅ Options for Deployment (Ranked by Simplicity → Flexibility)

### 1. Local Scheduled Runner

- ⏰ Use cron (Linux/macOS) or Task Scheduler (Windows) to run the script every X minutes

- ☁️ Keep API keys/secrets local

- 📦 Minimal setup

**Good for:** Solo use, dev phase, hobby machine

---

### 2. Self-hosted on VPS

- Deploy to a cheap server (e.g. Hetzner, DigitalOcean, Linode)

- Use `systemd`, cron, or a `supervisor` to keep the script running

- Add a `.env`, git pull, and done

**Good for:** Always-on pipeline, privacy control, light cost (~$5/mo)

---

### 3. Deploy via Serverless (Cloud Functions, AWS Lambda, etc.)

- Wrap modules as callable functions

- Use a scheduler (e.g., AWS EventBridge or Cloud Scheduler) to invoke periodically

- Store state in cloud storage (S3, Firestore, DynamoDB)

**Good for:** Pay-as-you-go, scale-to-zero, no server maintenance
**Challenge:** Trickier for things like file-based caching (`seen_videos.json` would need to move to cloud store)

---

### 4. Containerized MCP on Fly.io / Railway / Render

Dockerize the whole project

- Use a scheduler to invoke the orchestrator (Railway cron jobs, etc.)

- Add secrets via env vars

**Good for:** Mid-size ops, CI integration, clean logs, scalable

---

## 🧠 My Recommendation (for MVP)

Start with:

> 🔹 VPS (DigitalOcean/Hetzner) + `cron` + `.env` + `git` pull

Then if you want to grow:

- Containerize

- Move to Railway or Fly.io

- Add observability + multiple agents

---

## 🔐 Bonus Features We Might Add for Deployment

| Feature        | How                                      | Why                           |
| -------------- | ---------------------------------------- | ----------------------------- |
| `.env` manager | `dotenv`, secret manager                 | Secure and central config     |
| Logs           | Local file, stdout, or cloud log service | Trace/debug                   |
| Alerts         | Telegram or email on failure             | Peace of mind                 |
| Remote config  | Pull `config.yaml` from Git or remote    | Update feeds without redeploy |

---
