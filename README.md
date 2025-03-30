# 🧠 TechScry

TechScry monitors cutting-edge YouTube channels, summarizes AI/tech videos, scores them for relevance using LLMs, and delivers personalized daily digests and alerts to each user.

---

## 🚀 Features

- 🔎 **Video Discovery**: Scrapes RSS feeds of relevant YouTube channels
- 📝 **Transcription & Summarization**: Pulls transcripts and summarizes with OpenAI
- 📊 **Smart Scoring**: Uses GPT-3.5/4 to determine if a video is relevant to each user
- 📥 **Curated Digest Pool**: Relevant videos are queued until digest is sent
- 📧 **Digest Delivery**: Users receive a curated list of videos at scheduled times
- 👤 **User-Specific State**: Isolated digest queues, skipped videos, seen lists per user
- 🧠 **Summary Cache**: Prevents redundant LLM calls, improves cost efficiency

---

## 🏗️ Project Structure

```bash
techscry/
├── agents/              # Email agent (SMTP integration)
├── control_plane/       # Orchestration logic
│   └── orchestrator.py
├── modules/             # Core modules for fetch/summarize/score/cache
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── summary_cache.py
│   ├── skip_cache.py
│   ├── user_digest.py
│   ├── user_profile.py
│   └── channel_pool.py
├── templates/           # Digest HTML templates (email-safe and preview)
├── users/               # Per-user state
│   └── <user_id>/
│       ├── profile.json
│       ├── seen.json
│       ├── digest_queue.json
│       └── skipped.json
├── utils/               # Logging, cooldown, helper utils
├── scripts/             # Entry points for CLI usage
│   ├── run_pipeline.py
│   ├── send_curated_digest.py
│   └── send_digest.py (legacy)
├── data/                # Global logs and caches
│   ├── summary_log.jsonl
│   └── summary_cache.json
└── tests/
    └── mock/
        ├── mock_digest_data.json
        └── mock_skipped_videos.json
```

---

## 🔧 Setup

```bash
git clone https://github.com/YitzhakMizrahi/techscry.git
cd techscry
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=sk-xxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_app_password
```

Create a user profile:

```json
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

```bash
python scripts/run_pipeline.py [--verbose]
```

---

## 📬 Digest & Email

### Preview Email (Mock or Real)

```bash
python scripts/send_curated_digest.py --mock --preview
python scripts/send_curated_digest.py --preview
```

### Send Digest Email

```bash
python scripts/send_curated_digest.py
```

### Email-safe Version

```bash
python scripts/send_curated_digest.py --email-safe
```

---

## ⚙️ Flags Summary

| Flag           | Description                               |
| -------------- | ----------------------------------------- |
| `--mock`       | Use test data from `tests/mock/`          |
| `--preview`    | Render email HTML and open in browser     |
| `--email-safe` | Use stripped-down email-compatible styles |
| `--verbose`    | Log debug output and smart scorer prompts |

---

## 🧠 Architecture Highlights

### 🧩 Relevance Logic

| Type            | Trigger                          | Action                     |
| --------------- | -------------------------------- | -------------------------- |
| 🔔 Direct Match | Channel in `preferred_channels`  | Queue instantly            |
| 🧠 Smart Match  | Summary matches `keywords` (LLM) | Scored → queued or skipped |
| 🙅 Irrelevant   | Low score or no match            | Ignore                     |

### 💾 Caching

- `summary_cache.json`: Prevents re-summarizing the same video
- `summary_log.jsonl`: Audit log of summaries and scores

### 📦 Per-User State

- `seen.json`: Tracks previously processed videos
- `digest_queue.json`: Queued items for next digest email
- `skipped.json`: Videos with missing transcripts

---

## 🧭 Roadmap

- [ ] Cooldown enforcement before sending notifications ✅ (in progress)
- [ ] User setting to switch between real-time vs digest delivery
- [ ] CLI flags for mocking / faster dev iteration
- [ ] Web onboarding and dashboard
- [ ] Auto-generate RSS list from followed channels (YouTube API)
- [ ] Digest styling improvements (visual polish)

---

Built with ❤️ by TechScry Labs
