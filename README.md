# 🧠 TechScry

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

TechScry monitors cutting-edge YouTube channels, summarizes AI/tech videos, scores them for relevance using LLMs, and delivers personalized daily digests and alerts to each user.

---

## 🚀 Features

- 🔎 **Video Discovery**: Scrapes RSS feeds of relevant YouTube channels
- 📝 **Transcription & Summarization**: Pulls transcripts and summarizes with OpenAI
- 📊 **Smart Scoring**: Uses GPT-3.5/4 to determine if a video is relevant to each user
- 📥 **Digest Queue**: Collects top-scored videos for later delivery
- 📧 **Email Notifications**: Sends digest or instant alerts to each user
- 🧠 **Summary Caching**: Caches summaries to avoid duplicate LLM usage
- 👥 **Multi-User Support**: Each user has isolated preferences and state files
- ⚙️ **Cool-down & Notification Control**: Configurable per-user notification frequency

---

## 🏗️ Project Structure

```bash
techscry/
├── agents/                # Email (SMTP) integration
│   └── email_agent.py
├── control_plane/         # Pipeline orchestration
│   └── orchestrator.py
│   └── config.yaml         # Legacy static channel list (overridden by user config)
├── modules/              # Core system modules
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── skip_cache.py
│   ├── user_digest.py
│   ├── user_profile.py
│   ├── channel_pool.py
│   ├── summary_cache.py
├── scripts/              # CLI entry points
│   ├── run_pipeline.py
│   ├── send_digest.py         # Legacy global queue (deprecated)
│   └── send_curated_digest.py # New curated user-based digest
├── templates/            # Email digest HTML templates
│   ├── digest_email.html
│   └── digest_email_safe.html
├── users/                # Per-user state and preferences
│   └── default/
│       ├── profile.json
│       ├── seen.json
│       ├── digest_queue.json
│       ├── skipped.json
├── data/                 # Shared/global data
│   ├── summary_log.jsonl     # Global log of scored summaries
│   └── summary_cache.json    # Deduplicated LLM summary cache
├── tests/
│   └── mock/             # Mock digest/skipped data for dev
│       └── mock_digest_data.json
│       └── mock_skipped_videos.json
└── .env.template         # Sample environment file
```

---

## 🔧 Setup

1. **Clone the repo**

```bash
git clone https://github.com/YitzhakMizrahi/techscry.git
cd techscry
```

2. **Create & activate virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

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

## 🧪 Run the Pipeline

Run the full fetch → summarize → score → queue pipeline.

```bash
python scripts/run_pipeline.py
```

---

## 📬 Digest Delivery

### Preview Curated Digest (per-user queue)

```bash
python scripts/send_curated_digest.py --preview
```

### Send Curated Digest (real email)

```bash
python scripts/send_curated_digest.py
```

### Email-safe template

```bash
python scripts/send_curated_digest.py --email-safe
```

### Use mock data (for local testing only)

```bash
python scripts/send_digest.py --mock --preview
```

---

## ⚙️ Flags Summary

| Flag           | Description                               |
| -------------- | ----------------------------------------- |
| `--mock`       | Use test data from `tests/mock/`          |
| `--preview`    | Render HTML preview and open in browser   |
| `--email-safe` | Use inline styles for email compatibility |

You can combine flags like `--mock --preview` or `--email-safe --preview`.

---

## 💡 Architecture Notes

### Channel Source Strategy

- Channels are automatically aggregated from each user’s profile
- `channel_pool.py` builds a global pool of RSS feeds from all `preferred_channels`

### Relevance Logic

| Type            | Logic                  | Action                       |
| --------------- | ---------------------- | ---------------------------- |
| 🔔 Direct Match | Followed channel match | Skip scoring, queue directly |
| 🧠 Smart Match  | LLM matches keywords   | Add to digest (or alert)     |
| 🙅 Irrelevant   | Score below threshold  | Skip                         |

### Summary Caching

- `summary_cache.json` stores deduplicated summaries by `video_id`
- Reused if the same video is reprocessed later
- Reduces cost and speeds up re-runs

### Digest Queue

- Each user has their own `digest_queue.json`
- Curated based on scoring, preferences, and cooldown logic
- Only top N items are included in final delivery

---

## 📦 Backlog

- Responsive email design for mobile
- Scheduled task runner (hourly cron or loop)
- Retry queue for failed summaries
- Webhook/API onboarding
- Notification frequency tuning UI
- Real-time alert fallback mode (opt-in)

---

Built with ❤️ by TechScry Labs
