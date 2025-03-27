# 🧠 TechScry – AI-Powered Tech Signal Filter

TechScry is a modular, event-driven tool that listens to cutting-edge YouTube channels, summarizes new content, scores it for relevance, and notifies you only when it's noteworthy.

---

## 🚀 MVP Goal (Phase 1)

- ✅ Fetch new videos from a list of curated YouTube channels
- ✅ Retrieve transcripts (if available)
- 🔄 Summarize transcript using LLM (OpenAI API)
- 🔄 Score the content’s relevance (via keywords or AI)
- 🔄 Notify via email if score > threshold

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
│   └── notifier.py            # Notifies via agent
│
├── agents/                    # Agents that execute side effects
│   ├── email_agent.py         # Sends email via SMTP
│   ├── cli_logger.py          # Prints/logs locally
│   └── (optional) telegram.py # Future: Send message to Telegram
│
├── data/                      # Local state or cache
│   └── seen_videos.json       # Prevent duplicate notifications
│
├── utils/                     # Common helpers
│   └── chunking.py            # Break long text into LLM-friendly chunks
│
├── .env                       # Your keys/config (e.g., OpenAI, SMTP)
├── requirements.txt
└── README.md
```

## 📚 Modules Overview

| Module               | Description                                        |
| -------------------- | -------------------------------------------------- |
| `youtube_fetcher`    | Parses RSS feeds and returns unseen video metadata |
| `transcript_fetcher` | Gets transcript via `youtube-transcript-api`       |
| `summarizer`         | (Planned) Summarizes transcript using GPT          |
| `scorer`             | (Planned) Scores based on keywords or AI           |
| `notifier`           | (Planned) Chooses notification method              |

---

## ⚙️ Configuration

See `control_plane/config.yaml` for:

- YouTube channels
- Scoring thresholds (TBD)

---

## 🛠 Setup Instructions

1. Clone repo and set up venv
2. Install requirements: `pip install -r requirements.txt`
3. Add your `.env` file with OpenAI & SMTP creds (once ready)
4. Run test: `python modules/youtube_fetcher.py`

---

## 🗓️ Development Progress

- ✅ Project scaffolded and virtual environment set up
- ✅ RSS-based YouTube fetcher complete
- ✅ Transcript fetcher working
- ⏳ Summarizer module next
- 🔜 Scorer, notifier, and control loop

---

## 🧩 Vision

This project follows **Modular Control Plane (MCP)** principles:

- Modular design
- Event-driven
- Agent-based delivery
- Policy/scoring-driven filtering
