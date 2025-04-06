# 🧭 TechScry Risk Radar

A living document that outlines current and potential risks in building, scaling, or maintaining TechScry — both technically and strategically.

---

## 🧨 Product Risks

### 1. Redundancy vs Utility

- **Risk**: The app may duplicate the functionality of YouTube's own subscriptions or recommendation feed.
- **Mitigation**: Deliver signal-rich, fluff-free digests. Emphasize personalized scoring, transcript summarization, multi-source fusion, and distraction-free UI.

### 2. Overbuilding Without Use

- **Risk**: We could over-engineer (e.g., complex backend, multi-user auth, dashboards) without a clear value for you.
- **Mitigation**: Stay anchored in solving your daily workflow. Defer generalized features until there's real demand.

---

## 🧠 Cognitive Load Risks

### 3. Too Many Signals, Not Enough Filtering

- **Risk**: Adding Arxiv, HN, X, etc. could dilute the feed.
- **Mitigation**: Keep the digest curated, ranked, and optionally grouped by source or signal type.

### 4. Score Meaning Is Opaque

- **Risk**: Users may not trust or understand the "relevance" score.
- **Mitigation**: Add tooltip explanations (e.g. “You follow this channel”, “Keyword match: agents, langchain”).

---

## 🧱 Technical/Scaling Risks

### 5. JSON-Based Architecture Limits Scale

- **Risk**: Per-user JSON files won’t scale well beyond a few users or long-term usage.
- **Mitigation**: Acceptable for now. Consider migrating to Postgres (or Supabase) with a thin ORM layer later — as an experiment.

### 6. LLM Cost or Quota Constraints

- **Risk**: Relying on OpenAI for summarization and scoring may hit rate/cost limits.
- **Mitigation**: Summary caching + deduplication already in place. Explore offline or local LLMs later.

---

## 🔁 Maintainability / UX Debt

### 7. Frontend Diverges from Email Purpose

- **Risk**: The user digest page became a full-featured content UI. It could drift from its original preview/debug purpose.
- **Mitigation**: Embrace the shift. Treat the UI as your private feed. Repurpose email preview to mock/debug flows only.

### 8. Component Sprawl / Styling Inconsistency

- **Risk**: As we polish the UI further, duplicated logic or style drift may appear.
- **Mitigation**: Periodically refactor, centralize reusable components (e.g. badges, card layout, modal), and document UI guidelines.

---

## 🚀 Motivation Drift

### 9. Losing Track of Original Motivation

- **Risk**: If we focus too much on polish or theoretical scale, the project might lose its value for you.
- **Mitigation**: Regular check-ins (like this one). Recenter around “what’s useful to me this week?”

---

_Last updated: April 6, 2025_
