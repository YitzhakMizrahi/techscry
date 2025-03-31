# 🧠 TechScry

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

TechScry monitors cutting-edge YouTube channels, summarizes AI/tech videos, scores them for relevance using LLMs, and delivers personalized daily digests and alerts to each user.

---

## 🚀 Features

- 🔎 **Video Discovery**: Scrapes RSS feeds of relevant YouTube channels
- 🗘️ **Transcription & Summarization**: Pulls transcripts and summarizes with OpenAI
- 📊 **Smart Scoring**: Uses GPT-3.5/4 to determine if a video is relevant to each user
- 📅 **Cool-down & Queueing**: Limits how often users receive digest emails
- 🛅 **Digest Queue**: Stores high-quality videos for later batch delivery
- 📧 **Email Delivery**: Sends curated digests or real-time alerts
- 🧠 **Summary Caching**: Avoids re-summarizing the same video
- 👥 **Multi-User Support**: Per-user settings and isolated state files
- 🎓 **Dev Tools**: Mock mode, preview templates, flag-based CLI

---

## 🏠 Project Structure

```bash
techscry/
├── agents/                # Email (SMTP) integration
│   └── email_agent.py
├── control_plane/         # Pipeline orchestration
│   └── orchestrator.py
│   └── config.yaml        # Legacy static channel list (ignored by default)
├── modules/               # Core system modules
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── skip_cache.py
│   ├── user_digest.py
│   ├── user_profile.py
│   ├── channel_pool.py
│   ├── summary_cache.py
├── scripts/               # CLI entry points
│   ├── run_pipeline.py          # Full pipeline runner (multi-user)
│   ├── send_digest.py           # Legacy global queue sender (mockable)
│   └── send_curated_digest.py  # Current per-user digest sender
├── templates/            # Digest HTML templates
│   ├── digest_email.html
│   └── digest_email_safe.html
├── users/                # Per-user state and preferences
│   └── default/
│       ├── profile.json
│       ├── seen.json
│       ├── digest_queue.json
│       ├── skipped.json
├── utils
│    ├── __pycache__
│    ├── chunking.py
│    ├── logger.py 
│    └── notification_gate.py 
├── data/                 # Shared/global cache
│   ├── summary_log.jsonl     # All summaries (with score)
│   └── summary_cache.json    # LLM summary cache (by video_id)
├── tests/
│   └── mock/             # Mock data for development
│       ├── mock_digest_data.json
│       └── mock_skipped_videos.json
├── .env.template         # Example environment config
└── requirements.txt       # Python dependencies
```

---

## 🔧 Setup

1. **Clone the repo**

```bash
git clone https://github.com/YitzhakMizrahi/techscry.git
cd techscry
```

2. **Create & activate a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.template .env
```

Edit `.env` with your keys:

```env
OPENAI_API_KEY=sk-xxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_app_password
```

5. **Create a user profile**

```json
// users/default/profile.json
{
  "email": "your@email.com",
  "interests": {
    "keywords": ["openai", "gpt", "next.js"],
    "preferred_channels": ["OpenAI", "Fireship"]
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

## 🔮 Running the Pipeline

```bash
python scripts/run_pipeline.py
```

This fetches new videos, pulls transcripts, summarizes, scores relevance, and queues videos for later delivery.

---

## 📨 Digest Delivery

### Preview Curated Digest (per-user queue)

```bash
python scripts/send_curated_digest.py --preview
```

### Send Curated Digest (real email)

```bash
python scripts/send_curated_digest.py
```

### Email-safe version

```bash
python scripts/send_curated_digest.py --email-safe
```

### Use mock data for local testing

```bash
python scripts/send_digest.py --mock --preview
```

---

## ⚙️ CLI Flags Summary

| Flag           | Applies To               | Description                               |
| -------------- | ------------------------ | ----------------------------------------- |
| `--mock`       | `send_digest.py`         | Use mock data for preview/testing         |
| `--preview`    | `send_curated_digest.py` | Open HTML preview in browser              |
| `--email-safe` | Both senders             | Use inline styles for email compatibility |

Flags can be combined (e.g. `--email-safe --preview`).

---

## 💡 Architecture Notes

### Channel Aggregation

- Channels are pulled from all users’ `preferred_channels`
- Dynamically builds a global RSS feed pool

### Summary Caching

- `summary_cache.json` holds deduplicated summaries by video_id
- Reused when videos reappear to reduce LLM calls

### Smart Relevance

| Match Type     | Description                   | Action                         |
| -------------- | ----------------------------- | ------------------------------ |
| 🔔 Followed    | Channel in user profile       | Queue directly                 |
| 🧠 Smart Score | LLM determines high relevance | Add to digest (if cooldown OK) |
| ❌ Irrelevant  | Low score or no transcript    | Skipped                        |

### Digest Queue

- One queue per user
- Top videos sent based on score, freshness, cooldown
- Older entries retained for future selection

---

## 🌟 Ideas & Backlog

- Responsive digest email template
- Retry system for failed summaries
- Configurable scheduler (cron, loop, etc.)
- Live dashboard or admin panel
- Multi-source support (RSS, blogs, GitHub, etc.)
- Better mocking and test data fixtures
- Onboarding UI or API for user creation
- Discord or Slack notification integration (opt-in)

---

Built with ❤️ by TechScry Labs
