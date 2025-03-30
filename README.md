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
- 📬 **Digest System**: Queues relevant summaries into user-specific digests
- 📧 **Email Notifications**: Sends digest or instant alerts to each user
- 👥 **Multi-User Support**: Each user has isolated preferences and digest queues

---

## 🏗️ Project Structure

```bash
techscry/
├── agents/              # Email agent (SMTP integration)
├── control_plane/       # Orchestration logic (run_pipeline etc)
│   ├── orchestrator.py
│   ├── config.yaml      # Static fallback channel list
├── modules/             # Core modules (fetch, summarize, score)
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── user_digest.py
│   ├── user_profile.py
│   ├── skip_cache.py
│   ├── channel_pool.py
│   ├── summary_cache.py
├── utils/               # Logging, flags, gates, etc.
│   ├── logger.py
│   ├── notification_gate.py
├── templates/           # Digest HTML templates
├── users/               # Per-user state and config
│   └── <user_id>/
│       ├── profile.json
│       ├── seen.json
│       ├── digest_queue.json
│       ├── skipped.json
├── scripts/             # Executable scripts
│   ├── run_pipeline.py
│   ├── send_digest.py
│   ├── send_curated_digest.py
├── tests/
│   └── mock/
│       ├── mock_digest_data.json
│       └── mock_skipped_videos.json
├── data/                # Global logs
│   └── summary_log.jsonl
```

---

## 🔧 Setup

1. **Clone the repo**

```bash
git clone https://github.com/yourname/techscry.git
cd techscry
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create your .env**

```env
OPENAI_API_KEY=your_openai_key_here
MODEL_CHUNK=gpt-3.5-turbo
MODEL_MERGE=gpt-3.5-turbo
MAX_TOKENS_FOR_SAFE_SUMMARY=30000

SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_password
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

4. **Add a user**

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

### Run for All Users

```bash
python scripts/run_pipeline.py
```

### Run for One User + Verbose Mode

```bash
python scripts/run_pipeline.py --verbose
```

More dev flags (coming soon): `--mock`, `--limit`, etc.

---

## 📬 Digest & Email

### Preview Digest (with mock or real data)

```bash
python scripts/send_digest.py --mock --preview
python scripts/send_digest.py --preview
```

### Preview Final Curated Digest

```bash
python scripts/send_curated_digest.py --preview
```

### Send Digest Email

```bash
python scripts/send_digest.py
```

---

## 💡 Architecture Highlights

### Scoring Strategy

| Type              | Logic                           | Action                 |
| ----------------- | ------------------------------- | ---------------------- |
| 🔔 Direct Channel | User follows the channel        | Add to digest (direct) |
| 🧠 Smart Score    | LLM evaluates summary relevance | Score → Digest or Skip |
| 🙅 Irrelevant     | Low score                       | Ignore                 |

### User Isolation

Each user has their own:

- `seen.json`: Processed video IDs
- `digest_queue.json`: Pending digest items
- `skipped.json`: Skipped (e.g. no transcript)
- `profile.json`: Notification preferences

### Summary Efficiency

- All video summaries are cached in `data/summary_cache.json`
- Logs are kept in `data/summary_log.jsonl`
- Avoids repeated LLM calls

---

## 📦 Backlog Ideas

- User-facing UI for preferences
- Richer HTML with video thumbnails
- Telegram / WhatsApp delivery
- Digest scheduling and batching
- Webhook for new user onboarding

---

Built with ❤️ by TechScry Labs
