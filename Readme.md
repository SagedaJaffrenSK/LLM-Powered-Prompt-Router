### LLM-Powered Prompt Router for Intent Classification
- A Python service that intelligently routes user requests to specialized AI personas using a two-step Classify → Respond pattern.

# How It Works
User Message
     │
     ▼
┌─────────────────────┐
│  classify_intent()  │  ← Lightweight LLM call, returns JSON intent + confidence
└─────────────────────┘
     │
     ├── code     → 🧑‍💻 Code Expert
     ├── data     → 📊 Data Analyst
     ├── writing  → ✍️  Writing Coach
     ├── career   → 💼 Career Advisor
     └── unclear  → 🤔 Ask Clarifying Question
     │
     ▼
┌──────────────────────┐
│  route_and_respond() │  ← Second LLM call with expert system prompt
└──────────────────────┘
     │
     ▼
Final Response + route_log.jsonl entry

# Two-Step Process
- classify_intent(message) — Sends a short, focused prompt to the LLM asking it to return only {"intent": "...", "confidence": 0.0}. Optimized for speed and cost.
- route_and_respond(message, intent) — Looks up the matching expert system prompt and makes a second LLM call to generate a high-quality, context-aware response.


# Features

- 4 expert personas: Code Expert, Data Analyst, Writing Coach, Career Advisor
- Intent classification with confidence scoring
- Confidence threshold (0.7) — low-confidence intents fall back to unclear
- Manual override via @code, @data, @writing, @career prefixes
- Graceful error handling — malformed JSON defaults to unclear
- JSON Lines logging to route_log.jsonl
- Docker support

# Setup Instructions
 ## Prerequisites
 - Python 3.10+ or Docker
 - A free Groq API key

## 1. Clone the Repository
  - bashgit clone https://github.com/YOUR_USERNAME/llm-prompt-router.git
  # cd llm-prompt-router
## 2. Configure Environment Variables
  - bashcp .env.example .env
  - Edit .env and add your API key:
  # GROQ_API_KEY=your_actual_key_here
## 3a. Run Locally (Python)
- bashpip install -r requirements.txt

# Run all 15 test messages
- python main.py --test

# Run in interactive mode
- python main.py
## 3b. Run with Docker
- bash# Build and run test suite
- docker-compose up --build

# Or build manually
- docker build -t prompt-router .
- docker run --env-file .env prompt-router

# Usage
- Interactive Mode
## python main.py
- 🚀 LLM Prompt Router — Interactive Mode
- You: how do I sort a list in Python?
- 🔍 Intent: code  |  Confidence: 0.99
- 🤖 Response: [Code Expert response with production-quality code]

# Manual Intent Override
- Prefix your message with @intent to bypass the classifier:
- You: @data what is a standard deviation?
- [Router] Manual override detected: routing to 'data'

# Test Mode
## bash: python main.py --test
- Runs all 15 predefined test messages and logs results to route_log.jsonl.

# Logging
 - Every request is appended to route_log.jsonl in JSON Lines format:
 # json{"timestamp": "2026-03-08T15:11:17Z", "user_message": "how do i sort a list?", "intent": "code", "confidence": 0.99, "final_response": "..."}

# Design Decisions
- Groq + Llama 3 used instead of OpenAI due to free tier availability and speed. The architecture is provider-agnostic and can be switched by updating classifier.py and router.py.
- Confidence threshold of 0.7 ensures ambiguous messages always prompt clarification rather than a potentially wrong expert response.
- Prompts stored in prompts.py as a dictionary keyed by intent label — easy to extend with new personas without touching business logic.


# Dependencies
- groq
- python-dotenv