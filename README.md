# J.A.R.V.I.S.

### Just A Rather Very Intelligent System

A personal, offline-first AI assistant built for a Windows laptop with voice interaction, local computer control, persistent memory, and optional AI capabilities powered by Gemini.

---

## 🧠 About J.A.R.V.I.S.

J.A.R.V.I.S. is a personal AI assistant designed to combine traditional computer automation with modern AI capabilities.

The project is built around an **offline-first architecture**:

- Core computer-control features work locally.
- Voice recognition works locally using Vosk.
- Text-to-speech works locally using pyttsx3.
- Conversation history and memory are stored locally using PostgreSQL.
- Gemini is used as an optional online AI layer for general AI questions and reasoning.

The assistant is intentionally designed to be **manually launched** and does not automatically start with Windows.

---

## ✨ Features

### 🎤 Voice Assistant

- Offline speech recognition using Vosk
- Local microphone input
- Offline text-to-speech using pyttsx3
- Manual voice assistant launch
- Voice commands for supported computer operations

### 🖥️ Computer Control

J.A.R.V.I.S. can perform selected local computer operations such as:

- Open applications
- Open files
- Open folders
- Search for files
- List folder contents
- Get system information
- Get the current time
- Close supported applications
- Create folders with confirmation

The system does **not** expose unrestricted PowerShell or terminal execution through its general tool system.

---

## 🧠 Memory & Conversations

J.A.R.V.I.S. uses PostgreSQL for local data storage.

The backend supports:

- Conversations
- Conversation messages
- Persistent user memories
- Memory categories
- Memory importance
- Conversation summaries
- Conversation history

This allows J.A.R.V.I.S. to maintain context across conversations.

---

## 🤖 AI Capabilities

For general AI tasks, J.A.R.V.I.S. can use:

**Gemini 3.8 Flash**

Examples:

- Programming questions
- Technical explanations
- Reasoning
- Learning assistance
- General questions
- Writing assistance

Gemini is an **optional online layer**. The local computer-control system does not depend on Gemini.

---

## 🔌 Offline-First Architecture

The core assistant is designed to continue working when the internet or Gemini is unavailable.

### Offline

- React frontend
- FastAPI backend
- PostgreSQL
- Vosk speech recognition
- pyttsx3 text-to-speech
- Local command routing
- Windows computer control
- Local memory
- Conversation storage

### Online

- Gemini-powered AI responses
- Future cloud-based integrations

### Architecture

```text
                         J.A.R.V.I.S.
                              │
             ┌────────────────┴────────────────┐
             │                                 │
        React Frontend                    Voice Assistant
             │                                 │
             └────────────────┬────────────────┘
                              ↓
                         FastAPI Backend
                              │
          ┌───────────────────┼───────────────────┐
          ↓                   ↓                   ↓
      PostgreSQL          Local Tools          AI Layer
        OFFLINE             OFFLINE          Gemini 3.8
          │                   │               ONLINE
          ↓                   ↓                   ↓
      Memory &          Windows Laptop       AI Response
      Conversations       Control
```

---

## 🛠️ Tech Stack

### Frontend

- React
- JavaScript
- Vite
- Tailwind CSS
- GSAP
- Lenis
- Lucide React
- Fetch API

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Google Gemini API

### AI

- Gemini 3.8 Flash

### Voice

- Vosk
- PyAudioWPatch
- pyttsx3

### Development Tools

- Git
- GitHub
- VS Code
- Postman

---

## 📁 Project Structure

```text
jarvis/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── api/
│   │   ├── memory/
│   │   ├── tools/
│   │   ├── voice/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── models/
│   │   └── [local Vosk model - not committed]
│   │
│   ├── create_tables.py
│   ├── requirements.txt
│   └── start_jarvis_voice.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── tests/
│   ├── test_memory.py
│   ├── test_tool_router.py
│   └── test_tools.py
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── start_jarvis.bat
```

---

## 📌 Current Project Scope

This repository represents the **Basic V1 / Offline-First J.A.R.V.I.S. assistant**.

The current focus is:

- Personal laptop assistance
- Local computer control
- Voice interaction
- Persistent memory
- AI-assisted conversations
- Clean and modular architecture

Advanced capabilities are intentionally outside the current V1 scope.

---

## 🔮 Future Improvements

Possible future improvements include:

- Wake word detection
- More natural voice conversations
- Improved Hinglish/Hindi offline speech recognition
- Local LLM support
- Web search
- Vision capabilities
- Screen understanding
- Advanced AI agents
- More Windows automation
- Calendar integration
- Email integration
- Mobile companion application
- Multi-device control
- Advanced J.A.R.V.I.S. interface

---

## 📚 Learning Goals

This project is also a practical learning project covering:

- Full-stack development
- Python backend development
- REST APIs
- React development
- PostgreSQL
- SQLAlchemy
- AI API integration
- Speech recognition
- Text-to-speech
- Tool-based AI systems
- Memory systems
- Software architecture
- Git and GitHub
- Application security
- Windows automation

---

## 👨‍💻 Author

### AYUSH ANAND

B.Tech — Artificial Intelligence & Machine Learning

Interested in:

- Artificial Intelligence
- AI Engineering
- Full Stack Development
- Software Engineering
- Generative AI
- Intelligent Systems

---

## 📄 License

This project is currently intended as a personal/educational project.