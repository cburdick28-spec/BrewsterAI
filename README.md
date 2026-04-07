# BrewsterAI

A Streamlit-powered AI chatbot and information hub for **Brewster Madrid** — an American K-12 school with campuses in Madrid, Spain.

---

## Purpose

Prospective families often have dozens of questions before committing to a school visit: Where are the campuses? What curriculum does the school follow? What is the admissions process? When is the next open house?

**BrewsterAI** answers all of those questions instantly, in English or Spanish, 24 hours a day — without anyone needing to staff a help desk. It combines a retrieval-free knowledge base (all key school facts are baked directly into the AI system prompt) with a clean, tab-based Streamlit UI that surfaces structured information (FAQs, campus comparisons, events, academics, team bios) without requiring a chat interaction at all.

---

## Features

| Tab | What it does |
|-----|-------------|
| 💬 **Chat** | Streaming AI assistant powered by Claude. Answers any question about the school. Sidebar quick-question chips for one-click prompts. Per-message 👍/👎 feedback. |
| ❓ **FAQs** | Eight pre-written answers to the most common admissions questions — instant, no AI call. |
| 🏫 **Campuses** | Side-by-side comparison of all three locations with addresses, phone numbers, and character summaries. |
| 📅 **Events** | Upcoming open houses and info sessions with direct registration links. |
| ✅ **Apply Checklist** | Interactive step-by-step admissions checklist with progress bar. State persists across the session. |
| 👥 **Meet the Team** | Expandable bios for the four named school leaders, with gradient monogram avatars. |
| 📚 **Academics** | Per-division breakdown (Lower / Middle / Upper School) using the Brewster Model® framework. |

**Other highlights:**
- 🌐 Full English / Español language toggle (affects UI text and AI reply language)
- 🎨 Custom CSS (Playfair Display + DM Sans fonts, gold accent palette)
- 🔒 Privacy-first: no conversation transcripts are stored or exported

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI framework | [Streamlit](https://streamlit.io) ≥ 1.35 |
| AI model | [Anthropic Claude](https://www.anthropic.com) (`claude-sonnet-4-20250514`) via the `anthropic` Python SDK |
| Language | Python 3.10+ |

---

## Setup & Running Locally

### 1. Clone and install dependencies

```bash
git clone https://github.com/cburdick28-spec/BrewsterAI.git
cd BrewsterAI
pip install -r requirements.txt
```

### 2. Add your Anthropic API key

Create a file at `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

> You can get a key at [console.anthropic.com](https://console.anthropic.com).

### 3. Run the app

```bash
streamlit run brewster_chatbot.py
```

The app opens at `http://localhost:8501`.

---

## Deploying to Streamlit Cloud

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. In **Settings → Secrets**, add `ANTHROPIC_API_KEY = "sk-ant-..."`.
4. Click **Deploy**.

---

## Project Structure

```
BrewsterAI/
├── brewster_chatbot.py   # Main app — all UI, data, and AI logic
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

`brewster_chatbot.py` is organised into clearly delimited sections:

1. **Page config & CSS** — Streamlit page setup and custom styling
2. **Knowledge base** (`SCHOOL_KNOWLEDGE`) — raw school facts embedded in the AI prompt
3. **Prompt builder** (`build_system_prompt`) — constructs the Claude system prompt per language
4. **Static data** — `SUGGESTIONS`, `FAQS`, `EVENTS`, `STATS`, `CAMPUSES`, `CHECKLIST`, `NEWS`, `TEAM`, `SCHOOL_DIVISIONS`
5. **Helpers** — `get_client` (cached Anthropic client) and `stream_response` (streaming generator)
6. **Session state initialisation** — all keys set once on first load
7. **Sidebar** — language toggle, quick-question chips, clear-chat button
8. **Header** — branded title and divider
9. **Tab rendering** — one section per tab (Chat, FAQs, Campuses, Events, Checklist, Team, Academics)
