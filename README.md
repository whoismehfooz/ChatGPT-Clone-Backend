# 💬 ChatGPT Clone Backend

*> A production-minded backend for building stateful, multi-turn AI conversations with persistent chat history, context management, PostgreSQL, and asynchronous LLM execution.*

<p align="center">

🧠 Stateful Conversations • 💾 Persistent Chat History • 🧩 Context Management • 🤖 AI Execution • 🐘 PostgreSQL • 🔄 Alembic • 🐳 Docker Compose • ⚙️ CI

</p>

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM%20API-F55036?logo=groq&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Async%20ORM-D71F00?logo=sqlalchemy&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-51%20passing-success?logo=pytest&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

---

## 📖 Introduction

ChatGPT Clone Backend is a backend-focused implementation of a stateful conversational AI system.
Unlike a simple prompt-to-response API, this project maintains complete conversation state. User messages and assistant responses are persisted in PostgreSQL, previous messages are retrieved when a new message arrives, and a context builder prepares the relevant conversation history before sending it to the LLM.
The core flow is:
Client
  ↓
FastAPI
  ↓
Chat Service
  ↓
Conversation + Message Persistence
  ↓
Context Builder
  ↓
Groq LLM
  ↓
Assistant Response
  ↓
PostgreSQL

The project is designed around asynchronous request handling and separates API routes, services, repositories, database models, context construction, and AI execution.
2. ⚙️ Core Features & Technologies
Core Features
- 💬 Create and manage conversations
- 📨 Create and retrieve conversation messages
- 🔄 Stateful multi-turn conversations
- 🧠 Conversation context construction
- ✂️ Context token budgeting and truncation
- 🤖 Asynchronous LLM execution through Groq
- 🛡️ AI provider error handling
- 💾 Persistent PostgreSQL chat history
- 🔗 Conversation → Message relational structure
- 📄 Pagination for conversations and messages
- 🗃️ Database schema management with Alembic
- 📝 Request and AI execution logging
- 🧪 Unit, API, database, and integration testing
- 🐳 Docker and Docker Compose support
- 🔄 GitHub Actions CI with PostgreSQL
Technologies
Technology	Purpose
Python	Backend language
FastAPI	REST API framework
Pydantic	Request/response validation
SQLAlchemy Async	ORM and asynchronous database access
PostgreSQL	Persistent conversation storage
asyncpg	Async PostgreSQL driver
Alembic	Database migrations
Groq API	LLM execution
pytest	Testing
Docker	Application containerization
Docker Compose	Application + PostgreSQL orchestration
GitHub Actions	CI automation
---

## 🏗️ Project Architecture
```text
app/
├── api/
│   ├── chat.py
│   ├── conversation.py
│   ├── message.py
│   └── dependencies.py
│
├── core/
│   ├── config.py
│   └── logging_config.py
│
├── db/
│   ├── base.py
│   ├── dependencies.py
│   └── session.py
│
├── models/
│   ├── conversation.py
│   └── message.py
│
├── repositories/
│   ├── conversation_repository.py
│   └── message_repository.py
│
├── schemas/
│   ├── chat.py
│   ├── conversation.py
│   └── message.py
│
├── services/
│   ├── ai_service.py
│   ├── chat_service.py
│   ├── context_builder.py
│   ├── conversation_service.py
│   ├── message_service.py
│   └── token_counter.py
│
├── exceptions/
└── middleware/

migrations/
tests/
Dockerfile
docker-compose.yml
alembic.ini
pytest.ini
```

The main separation is:

API Layer
    →
Service Layer
    →
Repository Layer
    →
PostgreSQL

For AI requests:
Chat API
   →
ChatService
   →
MessageService
   →
ContextBuilder
   →
AIService
   →
Groq


---
## 🚀 How to Run & Use the Project

1. Clone the repository
git clone https://github.com/whoismehfooz/ChatGPT-Clone-Backend.git
cd ChatGPT-Clone-Backend

2. Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
cp .env.example .env

Open .env and configure your Groq API key:
GROQ_API_KEY=XXYYZZ

Keep your real API key private and never commit .env.
5. Start PostgreSQL and the application
docker compose build
docker compose up -d

Check the running containers:
docker compose ps

6. Apply database migrations
docker compose exec app alembic upgrade head

Verify the migration:
docker compose exec app alembic current

The current revision should show:
f49bb9aa1a4b (head)

7. Run the API
The application is now available through the Dockerized FastAPI service.
Open Swagger UI in your browser:
http://localhost:8000/docs

8. Use the API through Swagger
Start by creating a conversation:
POST /conversations
```text
Then use the returned conversation_id to:
GET  /conversations/{conversation_id}
GET  /conversations/{conversation_id}/messages
POST /conversations/{conversation_id}/messages
POST /conversations/{conversation_id}/chat
DELETE /conversations/{conversation_id}
```

For an actual AI conversation, use:
POST /conversations/{conversation_id}/chat
```text
with:
{
  "content": "Hello, introduce yourself."
}
```

The backend will:
Save user message
      →
Load conversation history
      →
Build LLM context
      →
Call Groq
      →
Save assistant response
      →
Return response


9. Run the tests
Normal test suite:
python -m pytest -q -m "not integration"

Integration tests:
python -m pytest -q -m integration

---
## 🗿 Final Note

A chatbot becomes a real backend when it remembers what happened before.

Built to move from single-shot AI calls → stateful conversational systems. 🚀