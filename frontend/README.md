# 🧠 TechScry Frontend

This is the **frontend interface** of TechScry, designed as a premium UI for browsing high-signal content feeds across platforms like YouTube, Arxiv, Hacker News, and more.

Built with [Next.js](https://nextjs.org), [Tailwind CSS](https://tailwindcss.com), [TypeScript](https://www.typescriptlang.org/), and [shadcn/ui](https://ui.shadcn.com/). Styled for clarity, performance, and delight.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
cd frontend
pnpm install
# or
npm install
```

### 2. Run the dev server

```bash
pnpm dev
```

Then open http://localhost:3000 in your browser.

## 📁 Project Structure

```bash
frontend/
├── app/                # App router layout
│   └── user/[userId]/  # Per-user feed route
├── components/         # Reusable UI
│   ├── DigestPreview.tsx
│   ├── SkippedVideos.tsx
│   ├── UserAdminPanel.tsx
│   └── VideoModal.tsx
├── mock/               # Local mock data (mirrors backend state)
├── lib/                # Utility functions
├── styles/             # Tailwind CSS + globals
└── shadcn/             # UI primitives via CLI (button, card, badge, etc.)


```

## 🧪 Local Testing Tips

- `mock/curation_pool.json` contains sample digest videos

- `mock/skipped.json` contains skipped videos (e.g. no transcript)

- **Routes:**

  - `/admin` → Admin dashboard (user controls, digest preview trigger)

  - `/user/<user_id>` → Personalized feed for user default

## 🎨 Tech & Tools

- ✅ shadcn/ui

- ✅ lucide-react

- ✅ TailwindCSS v4

- ✅ App Router (Next.js 15)

- ✅ TypeScript + ESLint

- ✅ Responsive layout, grid-based video display

- ✅ Modal YouTube player with keyboard & mouse support

## 🔗 Related

- [../README.md](../README.md) — Backend + system design notes
- [docs/ROADMAP.md](../docs/ROADMAP.md) — Development priorities
- [docs/RISK_RADAR.md](../docs/RISK_RADAR.md) — Risks and challenges
