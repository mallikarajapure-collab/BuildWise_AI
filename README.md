<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2563EB,45:6366F1,100:9333EA&height=230&section=header&text=BUILDWISE%20AI&fontSize=48&fontColor=FFFFFF&fontAlignY=36&desc=Discover%20Ideas%20%E2%80%A2%20Build%20Projects%20%E2%80%A2%20Grow%20Your%20Skills&descAlignY=59&descSize=15" width="100%" alt="BuildWise AI — Discover ideas, build projects, grow your skills" />

<p>
  <strong>A project discovery and learning assistant for your next build.</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Internship-GIST%20AI-6366F1?style=for-the-badge" alt="GIST AI Internship" />
  <img src="https://img.shields.io/badge/Task-01-2563EB?style=for-the-badge" alt="Task 1" />
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
</p>

</div>

---

## ✨ About BuildWise AI

**BuildWise AI** helps learners take the next step from *“What should I build?”* to *“How do I get started?”*

Created for **GIST AI Internship — Task 1: AI Basics, Intelligent Chatbot**, the project combines a Python-based chatbot with a React chat interface. It responds to common questions about project ideas, learning skills, roadmaps, and internship preparation.

> **How it works:** The current chatbot uses predefined, keyword-based rules. It is an educational assistant—not an LLM-powered chatbot.

## 🚀 What You Can Explore

| Capability | What it does |
|---|---|
| 💡 Project inspiration | Suggests starter ideas such as a study planner or portfolio analyzer |
| 🧭 Learning guidance | Recommends skills and tools to explore next |
| 🗺️ Project roadmaps | Breaks a project into practical starting steps |
| 🎯 Internship preparation | Shares portfolio, README, and project-explanation tips |
| 💬 Chat interface | Provides suggested prompts, message display, and fallback replies |
| 🛡️ Input handling | Handles blank messages, invalid input, and unknown questions |

The repository also contains the existing project-discovery experience and related saved-project and roadmap-progress work.

## 🎨 Project Identity

<div align="center">

| Colour | Hex | Role |
|:--:|:--:|---|
| <img src="https://placehold.co/18x18/2563EB/2563EB.png" alt="Blue swatch" /> | `#2563EB` | Primary blue — clarity and trust |
| <img src="https://placehold.co/18x18/6366F1/6366F1.png" alt="Indigo swatch" /> | `#6366F1` | Indigo — interactive accents |
| <img src="https://placehold.co/18x18/9333EA/9333EA.png" alt="Purple swatch" /> | `#9333EA` | Purple — creativity and discovery |
| <img src="https://placehold.co/18x18/0F172A/0F172A.png" alt="Slate swatch" /> | `#0F172A` | Deep slate — contrast and readability |

</div>

## 🧰 Tech Stack

- **Python** — chatbot logic and lightweight HTTP API.
- **React** — interactive chat experience.
- **Vite** — frontend development server and API proxy.
- **Streamlit** — used by the existing project-discovery application.
- **Pytest** — automated tests.

No external AI API key is required for the rule-based chatbot.

## ⚙️ Run Locally

### Prerequisites

- Python 3.10+ recommended
- Node.js and npm
- Git (optional, for cloning)

### 1. Get the code

```bash
git clone https://github.com/mallikarajapure-collab/BuildWise_AI.git
cd BuildWise_AI
```

If the project is already on your computer, open a terminal in its root folder instead.

### 2. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the chatbot API

From the project root, run:

```bash
python chatbot_api.py
```

The API listens at `http://127.0.0.1:8000`. Keep this terminal open.

### 4. Install frontend packages

Open a **second terminal** in the project root:

```bash
npm install
```

### 5. Start the frontend

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal. The API and frontend both need to be running for chatbot replies to work.

### Try asking

- `Hello`
- `Suggest a project`
- `What skills should I learn?`
- `Give me a roadmap`
- `How do I prepare for an internship?`

## 🔌 Chat API

**Endpoint:** `POST /api/chat`

**Request**

```json
{
  "message": "Give me a roadmap"
}
```

**Response shape**

```json
{
  "reply": "Your roadmap: ..."
}
```

During local development, Vite proxies `/api` requests to the Python server at `127.0.0.1:8000`.

## 🧪 Run Tests

From the repository root:

```bash
python -m pytest tests/ -v
```

The chatbot tests cover common intents, empty messages, unknown questions, and invalid input. The repository also includes project-recommender tests.

## 🧠 How It Works

```text
User message
    ↓
React chat interface
    ↓  POST /api/chat
Vite development proxy
    ↓
Python HTTP API
    ↓
Keyword and rule matching
    ↓
Predefined reply returned as JSON
    ↓
Reply displayed in chat
```

## ⚖️ Current Scope & Limitations

- Replies are selected from predefined responses; they are not generated by a large language model.
- The chatbot only recognises topics covered by its current keyword rules.
- Chat messages are kept in the current browser session; the chatbot API does not save conversation history to a server database.
- The local development server is intended for learning and demonstration, not public production deployment.

## 🌱 Project Context

- **Program:** GIST AI Internship
- **Task:** Task 1 — AI Basics: Intelligent Chatbot
- **Project:** BuildWise AI

---

<div align="center">

**Built to help turn a learning question into a project plan.**

<sub>Explore • Learn • Build • Repeat</sub>

</div>
