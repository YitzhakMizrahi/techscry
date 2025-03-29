# 🧠 TechScry

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
├── control_plane/       # Orchestration logic and run_pipeline()
│   ├── orchestrator.py
│   ├── config.yaml      # [Legacy] Static channel list (overridden at runtime)
├── modules/             # Core modules for fetch/summarize/score
│   ├── youtube_fetcher.py
│   ├── transcript_fetcher.py
│   ├── summarizer.py
│   ├── smart_scorer.py
│   ├── user_digest.py
│   ├── user_profile.py
│   ├── channel_pool.py  # 🆕 Collects preferred channels from all users
├── templates/           # Digest HTML templates (email-safe and browser preview)
├── users/               # Per-user data and preferences
│   ├── user123/
│       ├── profile.json
│       ├── seen.json
│       ├── digest_queue.json
│       ├── skipped.json
├── run_pipeline.py      # Main pipeline (single user or global run)
├── run_for_all_users.py # 🔁 Runs pipeline for all users in users/
├── send_digest.py       # Sends digest (with preview and mock flags)
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

3. **Configure environment**

Create a `.env` file:

```env
OPENAI_API_KEY=sk-xxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_app_password
```

4. **Add a user profile**

Create a directory in `users/` with a `profile.json` like this:

```json
{
  "email": "your@email.com",
  "interests": {
    "keywords": ["openai", "gpt", "next.js"],
    "preferred_channels": ["OpenAI", "Fireship"]
  },
  "notification_threshold": 0.6,
  "digest_threshold": 0.3
}
```

---

## 🧪 Run the Pipeline

### 🧵 For All Users

```bash
python run_for_all_users.py
```

### 🧪 For Single User (or dev/testing)

```bash
python run_pipeline.py
```

---

## 📬 Digest & Email

### Preview Email (mock data or real data)

```bash
python send_digest.py --mock --preview
python send_digest.py --preview
```

### Send Digest Email

```bash
python send_digest.py
```

### Email-safe version

```bash
python send_digest.py --email-safe
```

---

## ⚙️ Flags Summary

| Flag           | Description                                            |
| -------------- | ------------------------------------------------------ |
| `--mock`       | Use mock data from `mock/` for testing email digest    |
| `--preview`    | Open HTML preview in browser (write to `preview.html`) |
| `--email-safe` | Use email-compatible template (inlined styles)         |

Flags can be combined (e.g. `--mock --preview`, `--email-safe --preview`).

---

## 💡 Architecture Notes

### Channel Source Strategy

- Channels are **dynamically aggregated** from all user profiles.
- `channel_pool.py` reads all `users/<id>/profile.json` and builds the global pool.

### Relevance Logic

| Type            | Logic                           | Action                      |
| --------------- | ------------------------------- | --------------------------- |
| 🔔 Direct Match | Channel in `preferred_channels` | Instant alert, skip scoring |
| 🧠 Smart Match  | LLM score matches `keywords`    | Score → Digest or Alert     |
| 🙅 Irrelevant   | Low match                       | Skip                        |

### Storage

- Each user has:
  - `seen.json`: Tracks watched videos
  - `digest_queue.json`: Pending digest items
  - `skipped.json`: Skipped videos (e.g. no transcript)

---

## 📦 To Do (Backlog)

- Responsive digest styling
- Webhook/API for onboarding users
- User settings UI
- Retry queue for failed summarizations
- Embed video thumbnails in email

---

Built with ❤️ by TechScry Labs
