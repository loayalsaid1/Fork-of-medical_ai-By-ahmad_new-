# Medical AI Platform

> A comprehensive Django-based medical education platform with AI-powered learning assistance

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-0.4.1-purple.svg)](https://github.com/pgvector/pgvector)
[![Google AI](https://img.shields.io/badge/Gemini-AI-orange.svg)](https://ai.google.dev/)

## 🎯 Overview

This platform provides medical students with:
- 📚 **Structured Learning**: Hierarchical content (Years → Semesters → Modules → Subjects → Lessons)
- 🤖 **AI Assistant**: RAG-powered Q&A using Google Gemini + pgvector
- 📝 **Question Banks**: Multiple question types (MCQ, TBL, Flipped, Old Exams)
- 🎴 **Flashcards**: Spaced repetition learning system
- 📊 **Progress Tracking**: Streaks, study sessions, analytics
- 💳 **Subscriptions**: Tiered access control with free trials

## 📋 Documentation

- **[📖 Complete Documentation](DOCUMENTATION.md)** - Full technical documentation (15,000+ words)
- **[🧭 Navigation Guide](NAVIGATION_GUIDE.md)** - Quick reference for developers
- **[🚀 Setup Instructions](DOCUMENTATION.md#setup--installation)** - Environment setup

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          Client Applications                 │
│  ┌──────────────┐      ┌──────────────┐    │
│  │  Mobile App  │      │ Web Browser  │    │
│  │  (REST API)  │      │   (Django)   │    │
│  └──────┬───────┘      └──────┬───────┘    │
└─────────┼──────────────────────┼────────────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────────┐
│         Django Application Layer             │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   EDU    │  │  RAG_AI  │  │  USERS   │ │
│  │          │  │          │  │          │ │
│  │ Content  │  │ AI Chat  │  │   Auth   │ │
│  │ Questions│  │ Vector   │  │  Plans   │ │
│  │ Progress │  │ Search   │  │ Payments │ │
│  └──────────┘  └──────────┘  └──────────┘ │
│                                              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│           Data & AI Layer                    │
│                                              │
│  ┌────────────────┐    ┌─────────────────┐ │
│  │  PostgreSQL    │    │  Google Gemini  │ │
│  │  + pgvector    │    │  - Embeddings   │ │
│  │                │    │  - Generation   │ │
│  │ • Content DB   │    └─────────────────┘ │
│  │ • Vector Store │                         │
│  │ • User Data    │    ┌─────────────────┐ │
│  └────────────────┘    │  Google Cloud   │ │
│                        │    Storage      │ │
│                        │  - PDFs         │ │
│                        │  - Images       │ │
│                        └─────────────────┘ │
└─────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Django 5.2.5** - Web framework
- **Django REST Framework** - API
- **PostgreSQL** - Primary database
- **pgvector** - Vector similarity search
- **JWT Authentication** - Mobile auth

### AI/ML
- **Google Gemini** - LLM (gemini-2.5-flash-lite)
- **text-embedding-004** - 768-dim embeddings
- **RAG Pipeline** - Retrieval-Augmented Generation

### Storage
- **Google Cloud Storage** - PDFs, images
- **WhiteNoise** - Static files

### Production
- **Gunicorn** - WSGI server
- **Heroku/Railway** - Deployment ready

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone <repository-url>
cd medical_ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup PostgreSQL with pgvector
```sql
CREATE EXTENSION vector;
CREATE DATABASE medical_db;
```

### 3. Configure Environment
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=medical_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Google AI
GOOGLE_API_KEY=your-gemini-api-key
GEMINI_EMBED_MODEL=text-embedding-004
GEMINI_GEN_MODEL=gemini-2.5-flash-lite

# Google Cloud Storage
GS_BUCKET_NAME=your-bucket-name
GCS_CREDENTIALS_JSON={"type":"service_account",...}

# API
BASE_API_URL=http://localhost:8000/api
```

### 4. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 5. Create Vector Index
```sql
-- In psql
\c medical_db
CREATE INDEX ON rag_ai_chunk 
USING ivfflat (embedding_vec vector_cosine_ops) 
WITH (lists = 100);
```

### 6. Start Server
```bash
python manage.py runserver
```

Visit:
- **Web**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

## 📁 Project Structure

```
medical_ai/
├── 📂 edu/                    # Educational content
│   ├── models.py              # Years, Semesters, Modules, Subjects, Lessons, Questions
│   ├── views.py               # 40+ API endpoints
│   ├── serializers.py         # DRF serializers
│   └── policy.py              # Access control
│
├── 📂 rag_ai/                 # AI Question-Answering
│   ├── models.py              # Chunk (vector storage)
│   ├── qa.py                  # RAG algorithm
│   ├── views.py               # AI API
│   └── utils.py               # Usage tracking
│
├── 📂 users/                  # Auth & Subscriptions
│   ├── models.py              # User, Plan, Coupon, Streak
│   ├── views.py               # Auth, payments
│   ├── permissions.py         # Device binding
│   └── streak.py              # Activity tracking
│
├── 📂 web/                    # Web Interface
│   ├── views.py               # HTML views (2387 lines)
│   └── urls.py                # Web routing
│
├── 📂 medical_project/        # Django config
│   ├── settings.py            # Main settings
│   └── urls.py                # Root routing
│
├── 📂 templates/              # HTML templates
│   ├── base.html
│   ├── pages/
│   └── components/
│
├── 📄 requirements.txt        # Dependencies
├── 📄 Procfile                # Deployment
├── 📖 DOCUMENTATION.md        # Full docs
└── 🧭 NAVIGATION_GUIDE.md    # Developer guide
```

## 🔑 Key Features

### 1. RAG-Powered AI Chat
```python
# How it works:
1. User asks: "What is diabetes?"
2. Question → Gemini Embedding (768-dim vector)
3. pgvector searches similar chunks (cosine similarity)
4. Top K chunks → context for LLM
5. Gemini generates grounded answer
```

### 2. Hierarchical Content
```
Year 1-5
  └─ Semester 1,2
      └─ Module (Cardiovascular, Respiratory, etc.)
          └─ Subject (Anatomy, Physiology, etc.)
              └─ Chapter
                  └─ Lesson (with PDF, content, questions)
```

### 3. Subscription Tiers
- **Basic** (199 EGP/year): 10 AI queries/day, qbank questions
- **Premium** (399 EGP/year): 30 AI queries/day, exam review
- **Advanced** (599 EGP/year): 100 AI queries/day, all features

### 4. Multi-Interface
- **REST API**: JWT-authenticated, mobile-ready
- **Web App**: Session-based, full-featured interface

## 📡 API Examples

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student@example.com",
    "password": "secure123",
    "study_year": "y3"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "secure123",
    "device_id": "my-device-123"
  }'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Lessons
```bash
curl -X GET "http://localhost:8000/api/v1/edu/lessons/?subject_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-Device-Id: my-device-123"
```

### AI Chat
```bash
curl -X POST http://localhost:8000/api/v1/ask/simple/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-Device-Id: my-device-123" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What is the treatment for hypertension?",
    "k": 15
  }'

# Response:
{
  "question": "What is the treatment for hypertension?",
  "answer": "Treatment involves lifestyle modifications and medications...",
  "sources": [
    {"file_name": "cardiology.pdf", "chunk_index": 42, "distance": 0.23}
  ]
}
```

## 🔧 Common Tasks

### Add Initial Data
```python
# Django shell
python manage.py shell

from edu.models import Year
Year.objects.create(code='y1', name='Year 1', order=1)
Year.objects.create(code='y2', name='Year 2', order=2)
# ... etc

from users.models import Plan
Plan.objects.create(code='basic', name='Basic Plan', price_egp=199, duration_days=365, is_active=True)
# ... etc
```

### Ingest Documents for RAG
```python
# Create a script: scripts/ingest_pdf.py
from rag_ai.qa import embed_query
from rag_ai.models import Chunk
import PyPDF2

def ingest_pdf(file_path):
    # Extract text
    # Split into chunks
    # Embed each chunk
    # Save to database
    pass
```

### Check User Progress
```python
from users.models import User
from edu.models import LessonProgress

user = User.objects.get(username='student1')
completed = LessonProgress.objects.filter(user=user, is_done=True).count()
print(f"Lessons completed: {completed}")
```

## 📊 Database Schema (Simplified)

```sql
-- Content Hierarchy
Year → Semester → Module → Subject → Chapter → Lesson

-- Questions
Question (linked to Subject, Lesson, Chapter)
├── QuestionOption (for MCQs)
└── QuestionAttempt (user answers)

-- Learning Tools
FlashCard (user-created + admin)
FavoriteLesson
LessonProgress
PlannerTask

-- AI System
Chunk (file_name, content, embedding_vec[768])
DailyAIUsage (user, date, count)

-- Users & Subscriptions
User (extended AbstractUser)
├── Plan (subscription tiers)
├── Coupon (discounts)
└── UserStreak (activity tracking)
```

## 🔐 Security Features

- JWT authentication with refresh tokens
- Device binding (max 2 devices per user)
- Rate limiting on AI queries
- Plan-based access control
- CSRF protection
- HTTPS enforcement (production)
- Environment variable secrets

## 📈 Performance Optimizations

- **pgvector IVFFlat index**: Fast approximate nearest neighbor search
- **Database indexes**: On foreign keys, dates, frequently queried fields
- **Query optimization**: `select_related()`, `prefetch_related()`
- **Static file compression**: WhiteNoise
- **Connection pooling**: PostgreSQL

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test edu
python manage.py test rag_ai
python manage.py test users

# Run specific test class
python manage.py test edu.tests.TestQuestionViews
```

## 🚢 Deployment

### Heroku/Railway
```bash
# Already configured with:
# - Procfile (gunicorn)
# - requirements.txt
# - environment variables

# Just push:
git push heroku main
# or
railway up
```

### Environment Variables (Production)
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📚 Documentation

### For Developers
- **[Full Documentation](DOCUMENTATION.md)**: Complete technical specs (15,000+ words)
- **[Navigation Guide](NAVIGATION_GUIDE.md)**: Quick reference for finding code
- **Inline Comments**: Throughout the codebase

### For API Users
- API endpoints: See [API Endpoints](DOCUMENTATION.md#api-endpoints)
- Authentication: See [Authentication](DOCUMENTATION.md#authentication--authorization)
- Examples: See [API Examples](#api-examples) above

## 🤝 Contributing

1. Read [DOCUMENTATION.md](DOCUMENTATION.md) and [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md)
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test
4. Create migrations if needed: `python manage.py makemigrations`
5. Commit: `git commit -m "Add my feature"`
6. Push and create PR

## 📞 Support

- **Documentation**: [DOCUMENTATION.md](DOCUMENTATION.md)
- **Navigation**: [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md)
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **pgvector**: https://github.com/pgvector/pgvector
- **Google AI**: https://ai.google.dev/

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

- Django & DRF communities
- Google AI (Gemini)
- pgvector contributors
- PostgreSQL team

---

**Made with ❤️ for medical education**

**Last Updated**: December 24, 2025
