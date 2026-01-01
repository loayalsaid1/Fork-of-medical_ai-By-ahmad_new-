# Medical AI Platform - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Core Applications](#core-applications)
6. [Database Models](#database-models)
7. [API Endpoints](#api-endpoints)
8. [Authentication & Authorization](#authentication--authorization)
9. [Key Features](#key-features)
10. [Setup & Installation](#setup--installation)
11. [Navigation Guide](#navigation-guide)
12. [Development Workflow](#development-workflow)

---

## 🎯 Project Overview

This is a **Medical Education Platform** built with Django that provides:
- 📚 **Structured Learning Materials** organized by years, semesters, modules, subjects, chapters, and lessons
- 🤖 **AI-Powered Q&A System** using RAG (Retrieval-Augmented Generation) with pgvector
- 📝 **Question Banks** with multiple types (MCQs, TBL, Flipped, Old Exams)
- 🎴 **Flashcard System** for spaced repetition learning
- 📊 **Progress Tracking** with streaks and study sessions
- 💳 **Subscription Management** with multiple pricing tiers
- 🌐 **Dual Interface**: REST API for mobile apps + Web interface

---

## 🏗️ Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Client Layer                        │
│  ┌──────────────┐         ┌──────────────┐         │
│  │  Mobile App  │         │  Web Browser │         │
│  │   (API)      │         │   (Django)   │         │
│  └──────────────┘         └──────────────┘         │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Django Application Layer                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │   EDU    │ │  RAG_AI  │ │  USERS   │  [APPS]   │
│  └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                 Data Layer                           │
│  ┌──────────────┐         ┌──────────────┐         │
│  │  PostgreSQL  │         │  Google AI   │         │
│  │  + pgvector  │         │   (Gemini)   │         │
│  └──────────────┘         └──────────────┘         │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                Storage Layer                         │
│  ┌──────────────────────────────────────┐           │
│  │  Google Cloud Storage (GCS)          │           │
│  │  - PDFs, Images, Media Files         │           │
│  └──────────────────────────────────────┘           │
└─────────────────────────────────────────────────────┘
```

### Request Flow
1. **Mobile App** → JWT Auth → REST API endpoints
2. **Web Browser** → Session Auth → Django Views → Templates
3. **AI Queries** → Gemini Embeddings → pgvector Search → LLM Generation

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.5
- **API**: Django REST Framework 3.16.1
- **Database**: PostgreSQL with pgvector extension
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Storage**: Google Cloud Storage
- **Server**: Gunicorn (production)

### AI/ML
- **LLM**: Google Gemini (gemini-2.5-flash-lite)
- **Embeddings**: text-embedding-004 (768 dimensions)
- **Vector Search**: pgvector with IVFFlat index

### Frontend
- **Templates**: Django Templates
- **Rich Text**: CKEditor
- **Static Files**: WhiteNoise

### Key Libraries
```
Django==5.2.5
djangorestframework==3.16.1
psycopg2-binary==2.9.10
pgvector==0.4.1
google-generativeai==0.8.5
django-storages==1.14.6
google-cloud-storage==3.4.1
gunicorn==23.0.0
```

---

## 📁 Project Structure

```
medical_ai/
│
├── 🚀 manage.py                    # Django management script
├── 🌐 Procfile                     # Deployment config (Heroku/Railway)
├── 📦 requirements.txt             # Python dependencies
│
├── 📂 medical_project/             # Main project configuration
│   ├── settings.py                 # Django settings (DB, APPS, STORAGE)
│   ├── urls.py                     # Root URL routing
│   ├── wsgi.py                     # WSGI entry point
│   ├── asgi.py                     # ASGI entry point
│   └── admin_menu.py               # Admin interface customization
│
├── 📂 edu/                         # Education/Learning module
│   ├── models.py                   # Year, Semester, Module, Subject, Lesson, Question, FlashCard
│   ├── views.py                    # API views for learning materials
│   ├── serializers.py              # DRF serializers
│   ├── urls.py                     # API routing
│   ├── policy.py                   # Access control policies
│   ├── admin.py                    # Admin configurations
│   └── migrations/                 # Database migrations
│
├── 📂 rag_ai/                      # AI Question-Answering system
│   ├── models.py                   # Chunk (vector storage)
│   ├── views.py                    # AI chat endpoints
│   ├── qa.py                       # RAG logic (embedding, search, generation)
│   ├── utils.py                    # AI usage tracking
│   ├── urls.py                     # AI API routing
│   └── migrations/
│
├── 📂 users/                       # User management & subscriptions
│   ├── models.py                   # User, Plan, Coupon, UserStreak
│   ├── views.py                    # Auth, subscriptions, payments
│   ├── serializers.py              # User serializers
│   ├── permissions.py              # Custom permissions (SingleDeviceOnly)
│   ├── streak.py                   # Activity streak tracking
│   ├── services.py                 # Business logic
│   ├── urls.py                     # Auth/subscription routing
│   └── migrations/
│
├── 📂 web/                         # Web interface (HTML views)
│   ├── views.py                    # Web pages (landing, materials, questions)
│   ├── urls.py                     # Web routing
│   ├── admin.py
│   ├── models.py                   # (Minimal/none)
│   └── migrations/
│
├── 📂 templates/                   # Django HTML templates
│   ├── base.html                   # Base template
│   ├── landing_page.html           # Homepage
│   ├── _partials/                  # Reusable components
│   ├── admin/                      # Admin customizations
│   ├── components/                 # UI components
│   └── pages/                      # Page templates
│
├── 📂 static/                      # Static files (CSS, JS, images)
│   ├── ckeditor/                   # Rich text editor assets
│   └── logos/
│
├── 📂 staticfiles/                 # Collected static files (production)
│
└── 📂 uploads/                     # User uploads (if not using GCS)
```

---

## 🔧 Core Applications

### 1. **EDU** - Educational Content Management

**Purpose**: Manages the hierarchical structure of medical education content

**Key Models**:
```
Year → Semester → Module → Subject → Chapter → Lesson
                                              ↓
                                          Question
                                          FlashCard
```

**Responsibilities**:
- Content organization (years, semesters, modules, subjects)
- Lesson management with PDF attachments
- Question bank with multiple types
- Flashcard system (user-created & admin-created)
- Progress tracking (LessonProgress)
- Study planner (PlannerTask)
- Favorite lessons
- Question attempts and study sessions

**Access Control**:
- Visibility based on user's `study_year`
- Plan-based restrictions (basic, premium, advanced)
- Module `is_ready` flag

---

### 2. **RAG_AI** - AI-Powered Question Answering

**Purpose**: RAG (Retrieval-Augmented Generation) system for medical queries

**How It Works**:
1. **Ingestion**: Medical textbooks/PDFs chunked and embedded
2. **Storage**: Vectors stored in PostgreSQL with pgvector
3. **Query**: User question → embedded → vector similarity search
4. **Generation**: Retrieved chunks → Gemini LLM → answer

**Key Components**:
- `Chunk` model: Stores text chunks with embeddings
- `qa.py`: Core RAG logic
  - `embed_query()`: Convert text to vectors
  - `search_top_k()`: pgvector cosine similarity search
  - `ask()`: Generate answer with LLM
- `DailyAIUsage`: Track daily AI query limits per user

**Performance**:
- IVFFlat index for fast approximate search
- Configurable `probes` parameter (accuracy vs speed)
- Daily usage limits based on subscription plan

---

### 3. **USERS** - Authentication & Subscriptions

**Purpose**: User management, authentication, and monetization

**Key Models**:
- `User`: Custom user with study year, plan, subscription status
- `Plan`: Subscription tiers (none, basic, premium, advanced)
- `Coupon`: Discount codes with percentage off
- `UserStreak`: Daily activity tracking
- `Payment`: Payment transaction records

**Features**:
- JWT authentication for mobile apps
- Session authentication for web
- **Device binding**: Users limited to 2 devices
- Free trial system
- Subscription purchase flow
- Coupon validation and application
- Streak tracking (Cairo timezone)

**Subscription Tiers**:
```
├── None:     No access
├── Basic:    10 AI queries/day, qbank questions
├── Premium:  30 AI queries/day, qbank + exam_review
└── Advanced: 100 AI queries/day, all question types
```

---

### 4. **WEB** - User Interface

**Purpose**: HTML-based web interface for students

**Features**:
- Landing page
- Registration and login
- Materials browser (hierarchical navigation)
- Lesson viewer with PDF
- Question browser with filters
- Flashcard management
- Study planner
- Favorites and progress tracking
- Pomodoro timer logs

**Tech**:
- Django templates with partials
- HTMX for dynamic updates (likely)
- Bootstrap/custom CSS

---

## 🗄️ Database Models

### EDU App Models

#### Hierarchy Models
```python
Year
├── code: CharField (y1, y2, y3, y4, y5)
├── name: CharField
└── order: PositiveIntegerField

Semester
├── year: ForeignKey → Year
├── name: CharField
└── order: PositiveIntegerField

Module
├── semester: ForeignKey → Semester
├── name: CharField
├── order: PositiveIntegerField
└── is_ready: BooleanField (visibility flag)

Subject
├── module: ForeignKey → Module
├── name: CharField
└── order: PositiveIntegerField

Chapter
├── subject: ForeignKey → Subject
├── title: CharField
└── order: PositiveIntegerField

Lesson
├── subject: ForeignKey → Subject
├── chapter: ForeignKey → Chapter (optional)
├── title: CharField
├── description: TextField
├── content: TextField (CKEditor HTML)
├── pdf: FileField (GCS)
├── order: PositiveIntegerField
├── part_type: CharField (theoretical/practical)
└── created_at: DateTimeField
```

#### Question Model
```python
Question
├── subject: ForeignKey → Subject
├── lesson: ForeignKey → Lesson (optional)
├── chapter: ForeignKey → Chapter (optional)
├── text: TextField (CKEditor HTML)
├── image: ImageField (optional, GCS)
├── answer_text: TextField (CKEditor HTML)
├── source: CharField (qbank, exam_review, old_exam, tbl, flipped)
├── module: CharField
├── part_type: CharField (theoretical/practical)
├── is_tbl: BooleanField
├── is_flipped: BooleanField
└── exam_year: PositiveIntegerField (optional)

QuestionOption (for MCQs)
├── question: ForeignKey → Question
├── text: CharField
├── is_correct: BooleanField
└── order: PositiveIntegerField
```

#### Learning Tools
```python
FlashCard
├── lesson: ForeignKey → Lesson
├── front: TextField
├── back: TextField
├── owner_type: CharField (admin/user)
├── owner: ForeignKey → User
├── created_at: DateTimeField
└── INDEX on (owner_type, owner)

FavoriteLesson
├── user: ForeignKey → User
├── lesson: ForeignKey → Lesson
└── created_at: DateTimeField

LessonProgress
├── user: ForeignKey → User
├── lesson: ForeignKey → Lesson
├── is_done: BooleanField
└── marked_at: DateTimeField

PlannerTask
├── user: ForeignKey → User
├── title: CharField
├── description: TextField (optional)
├── due_date: DateField
├── is_done: BooleanField
└── created_at: DateTimeField
```

#### Study Analytics
```python
StudySession
├── user: ForeignKey → User
├── started_at: DateTimeField
├── ended_at: DateTimeField (nullable)
└── total_questions: PositiveIntegerField

QuestionAttempt
├── session: ForeignKey → StudySession
├── question: ForeignKey → Question
├── user_answer: CharField (optional)
├── is_correct: BooleanField (nullable)
└── attempted_at: DateTimeField
```

---

### RAG_AI App Models

```python
Chunk
├── file_name: CharField
├── chunk_index: IntegerField
├── content: TextField (actual text content)
├── embedding: BinaryField (legacy, not used)
├── embedding_vec: VectorField(768) (pgvector)
├── faiss_id: IntegerField (legacy FAISS index)
└── UNIQUE (file_name, chunk_index)

DailyAIUsage
├── user: ForeignKey → User
├── date: DateField
├── count: PositiveIntegerField
└── UNIQUE (user, date)
```

---

### USERS App Models

```python
User (AbstractUser)
├── phone_number: CharField (optional)
├── study_year: CharField (y1-y5)
├── plan: CharField (none/basic/premium/advanced)
├── is_active_subscription: BooleanField
├── activated_at: DateTimeField (nullable)
├── expires_at: DateTimeField (nullable)
├── device_id_1: CharField (device binding)
├── device_id_2: CharField (device binding)
└── active_device_id: CharField (currently active device)

Plan
├── code: CharField (matches User.Plan choices)
├── name: CharField
├── price_egp: DecimalField
├── duration_days: PositiveIntegerField
└── is_active: BooleanField

Coupon
├── code: CharField (unique)
├── percent: DecimalField (0-100)
├── valid_from: DateTimeField (nullable)
├── valid_to: DateTimeField (nullable)
├── is_active: BooleanField
├── max_uses_total: PositiveIntegerField (nullable)
└── used_count_total: PositiveIntegerField

UserStreak
├── user: OneToOneField → User
├── current_streak: PositiveIntegerField
└── last_active_date: DateField

Payment
├── user: ForeignKey → User
├── plan: ForeignKey → Plan
├── amount: DecimalField
├── status: CharField (pending/completed/failed)
├── transaction_id: CharField (unique)
└── created_at: DateTimeField
```

---

## 🔌 API Endpoints

### Authentication (`/api/auth/`)
```
POST   /api/auth/register/          # Register new user
POST   /api/auth/login/             # Login with device_id
POST   /api/auth/refresh/           # Refresh JWT token
GET    /api/auth/me/                # Get current user info
```

### Educational Content (`/api/v1/edu/`)

#### Content Hierarchy
```
GET    /api/v1/edu/years/me/               # User's year
GET    /api/v1/edu/semesters/              # Semesters for user's year
GET    /api/v1/edu/modules/                # Modules (filtered by semester_id)
GET    /api/v1/edu/subjects/               # Subjects (filtered by module_id)
GET    /api/v1/edu/chapters/               # Chapters (filtered by subject_id)
GET    /api/v1/edu/lessons/                # Lessons (filtered by subject_id/chapter_id)
GET    /api/v1/edu/lessons/:id/            # Lesson detail with content
```

#### Questions
```
GET    /api/v1/edu/questions/              # List questions (filters: source, module, etc.)
GET    /api/v1/edu/questions/:id/          # Question detail
GET    /api/v1/edu/exam-years/             # Available exam years for old questions
POST   /api/v1/edu/questions/:id/reveal/   # Reveal answer (consumes action)
```

#### Study Sessions & Attempts
```
POST   /api/v1/edu/study-sessions/         # Create study session
POST   /api/v1/edu/question-attempts/      # Submit question attempt
GET    /api/v1/edu/question-attempts/stats/ # Get attempt statistics
```

#### Flashcards
```
GET    /api/v1/edu/flashcards/             # List flashcards (filtered by lesson_id)
POST   /api/v1/edu/flashcards/             # Create flashcard
GET    /api/v1/edu/flashcards/:id/         # Flashcard detail
PUT    /api/v1/edu/flashcards/:id/         # Update flashcard
DELETE /api/v1/edu/flashcards/:id/         # Delete flashcard
GET    /api/v1/edu/flashcards/count/       # Count user's flashcards
```

#### Progress Tracking
```
GET    /api/v1/edu/lessons/progress/count/ # Count completed lessons
POST   /api/v1/edu/lessons/:id/progress/done/ # Mark lesson as done
GET    /api/v1/edu/lessons/progress/ids/   # IDs of completed lessons
GET    /api/v1/edu/lessons/progress/       # List lesson progress with details
```

#### Favorites
```
GET    /api/v1/edu/favorites/lessons/      # List favorite lessons
POST   /api/v1/edu/favorites/lessons/add/  # Add favorite
DELETE /api/v1/edu/favorites/lessons/remove/ # Remove favorite
GET    /api/v1/edu/favorites/lessons/ids/  # IDs of favorite lessons
```

#### Planner
```
GET    /api/v1/edu/planner/tasks/          # List all tasks
POST   /api/v1/edu/planner/tasks/          # Create task
GET    /api/v1/edu/planner/tasks/today/    # Tasks due today
POST   /api/v1/edu/planner/tasks/:id/done/ # Mark done
POST   /api/v1/edu/planner/tasks/:id/undone/ # Mark undone
DELETE /api/v1/edu/planner/tasks/:id/      # Delete task
```

#### Activity Tracking
```
GET    /api/v1/edu/streak/message/         # Get streak info
GET    /api/v1/edu/home-dashboard/         # Dashboard stats (streaks, progress)
GET    /api/v1/edu/materials/home/         # Materials home stats
```

---

### AI Chat (`/api/v1/`)
```
POST   /api/v1/ask/                        # AI chat (full response)
POST   /api/v1/ask/simple/                 # AI chat (simple response)

Request Body:
{
  "q": "What is the treatment for hypertension?",
  "k": 15,              // optional: chunks to retrieve
  "probes": 10,         // optional: IVFFlat probes
  "max_chars": 5000     // optional: max context chars
}

Response:
{
  "question": "...",
  "answer": "...",
  "sources": [
    {"file_name": "...", "chunk_index": 1, "distance": 0.23}
  ],
  "usage": {
    "embedding_model": "text-embedding-004",
    "generation_model": "gemini-2.5-flash-lite",
    "k": 15,
    "elapsed_ms": 1234
  },
  "trace_id": "uuid"
}
```

---

### Subscriptions (`/api/`)
```
GET    /api/plans/                         # List available plans
POST   /api/subscriptions/start-trial/     # Start free trial
POST   /api/subscriptions/purchase/        # Purchase subscription
POST   /api/coupons/validate/              # Validate coupon code
POST   /api/payments/create/               # Create payment record
```

---

## 🔐 Authentication & Authorization

### Authentication Methods

#### 1. **JWT for Mobile Apps**
```python
# Login
POST /api/auth/login/
{
  "username": "student123",
  "password": "password",
  "device_id": "mobile-device-uuid"
}

Response:
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi..."
}

# Use in requests
Authorization: Bearer eyJ0eXAi...
```

#### 2. **Session for Web**
- Traditional Django session authentication
- Login sets `request.session['access']` and `request.session['device_id']`

---

### Authorization Policies

#### Device Binding (`SingleDeviceOnly` permission)
- Users can register up to 2 devices
- Only 1 device can be active at a time
- Enforced via `X-Device-Id` header
- Prevents account sharing

#### Plan-Based Access (in `edu/policy.py`)

**Basic Plan**:
- 10 AI queries per day
- Access to `qbank` questions only

**Premium Plan**:
- 30 AI queries per day
- Access to `qbank` + `exam_review` questions
- Admin flashcards visible

**Advanced Plan**:
- 100 AI queries per day
- Access to all question types (qbank, exam_review, tbl, flipped, old_exam)
- All features unlocked

#### Content Visibility
- Users only see content for their `study_year`
- Modules must have `is_ready=True`
- Active subscription required (`is_active_subscription=True`)

---

## ✨ Key Features

### 1. **Hierarchical Content Organization**
Medical curriculum organized in 6 levels:
```
Year (y1-y5) → Semester → Module → Subject → Chapter → Lesson
```

Benefits:
- Easy navigation
- Progressive learning
- Clear structure for medical education

---

### 2. **RAG-Based AI Assistant**

**Technical Implementation**:
```python
# 1. Embedding (query)
query_vector = embed_query("What is diabetes?")  # 768-dim vector

# 2. Vector Search (pgvector)
similar_chunks = search_top_k(query_vector, k=15)
# Uses IVFFlat index with cosine similarity

# 3. Context Building
context = "\n\n".join(chunk.content for _, chunk in similar_chunks[:5000])

# 4. LLM Generation (Gemini)
prompt = f"""You are a medical AI assistant.
Context: {context}
Question: {user_question}
Answer:"""
answer = gemini_model.generate(prompt)
```

**Advantages**:
- Grounds answers in actual medical textbooks
- Reduces hallucination
- Provides source attribution
- Scalable to large document corpora

---

### 3. **Multi-Type Question Bank**

**Question Sources**:
- `qbank`: Standard question bank
- `exam_review`: Exam-focused questions
- `old_exam`: Past exam questions (by year)
- `tbl`: Team-Based Learning
- `flipped`: Flipped classroom questions

**Question Features**:
- Rich text with images (CKEditor)
- Multiple choice options
- Detailed explanations
- Linked to lessons and chapters
- Reveal answer (tracked action)

---

### 4. **Intelligent Flashcard System**

**Two Types**:
1. **Admin Flashcards**: Pre-made by instructors
2. **User Flashcards**: Student-created notes

**Features**:
- Linked to lessons
- Front/back format (spaced repetition ready)
- Plan-based visibility
- Database indexed for fast filtering

---

### 5. **Progress Tracking & Gamification**

**Streak System** (`users/streak.py`):
- Daily activity tracking
- Cairo timezone aware
- Automatic increment for consecutive days
- Reset on missed days

**Progress Metrics**:
- Lessons completed (`LessonProgress`)
- Questions attempted (`QuestionAttempt`)
- Study time tracking (`StudySession`)
- Flashcard count
- Favorite count

**Dashboard**:
- Current streak
- Weekly activity
- Completion percentages
- Recent activity

---

### 6. **Study Planner**
- Create tasks with due dates
- Mark complete/incomplete
- Filter by date (today, upcoming)
- Linked to lessons (optional)

---

### 7. **Subscription & Monetization**

**Free Trial Flow**:
```
1. User registers
2. Calls /api/subscriptions/start-trial/
3. Gets 7-day trial of Basic plan
4. Expires_at set automatically
```

**Purchase Flow**:
```
1. Browse /api/plans/
2. (Optional) Validate coupon /api/coupons/validate/
3. Purchase /api/subscriptions/purchase/
   - Apply coupon discount
   - Create Payment record
4. Activate subscription
   - Set is_active_subscription=True
   - Set expires_at = now + plan.duration_days
```

**Revenue Features**:
- Multiple pricing tiers
- Percentage-based coupons
- Usage limits on coupons
- Time-limited offers
- Payment tracking

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Google Cloud Platform account (for GCS)
- Google AI API key (for Gemini)

### 1. Clone & Environment Setup
```bash
git clone <repository-url>
cd medical_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. PostgreSQL Setup
```sql
-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create database
CREATE DATABASE medical_db;
```

### 3. Environment Variables
Create `.env` file:
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CSRF_TRUSTED_ORIGINS=http://localhost,https://yourdomain.com

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

# Cloudinary (optional, if not using GCS)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Security
SECURE_SSL_REDIRECT=False  # Set True in production
SESSION_COOKIE_SECURE=False  # Set True in production
CSRF_COOKIE_SECURE=False  # Set True in production

# API Settings
BASE_API_URL=http://localhost:8000/api
WEB_DEVICE_ID=web-device-1
```

### 4. Database Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Create Vector Index (pgvector)
```sql
-- Connect to database
\c medical_db

-- Create IVFFlat index for fast vector search
CREATE INDEX ON rag_ai_chunk 
USING ivfflat (embedding_vec vector_cosine_ops) 
WITH (lists = 100);
-- Adjust 'lists' based on data size: sqrt(rows) is a good starting point
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit:
- Web: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

---

### 9. Initial Data Setup

**Create Years**:
```python
from edu.models import Year

Year.objects.create(code='y1', name='Year 1', order=1)
Year.objects.create(code='y2', name='Year 2', order=2)
Year.objects.create(code='y3', name='Year 3', order=3)
Year.objects.create(code='y4', name='Year 4', order=4)
Year.objects.create(code='y5', name='Year 5', order=5)
```

**Create Subscription Plans**:
```python
from users.models import Plan

Plan.objects.create(
    code='basic',
    name='Basic Plan',
    price_egp=199.00,
    duration_days=365,
    is_active=True
)

Plan.objects.create(
    code='premium',
    name='Premium Plan',
    price_egp=399.00,
    duration_days=365,
    is_active=True
)

Plan.objects.create(
    code='advanced',
    name='Advanced Plan',
    price_egp=599.00,
    duration_days=365,
    is_active=True
)
```

---

### 10. Loading RAG Content

**Ingestion Script** (you'll need to create this):
```python
# scripts/ingest_documents.py
import PyPDF2
from rag_ai.models import Chunk
from rag_ai.qa import embed_query
import numpy as np

def chunk_text(text, chunk_size=500):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - 50):  # 50 word overlap
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_pdf(file_path):
    """Ingest a PDF file into the RAG system"""
    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    chunks = chunk_text(text)
    file_name = os.path.basename(file_path)
    
    for idx, chunk_text in enumerate(chunks):
        embedding = embed_query(chunk_text)
        Chunk.objects.create(
            file_name=file_name,
            chunk_index=idx,
            content=chunk_text,
            embedding_vec=embedding.tolist()
        )
    
    print(f"Ingested {len(chunks)} chunks from {file_name}")

# Usage
ingest_pdf('path/to/medical_textbook.pdf')
```

---

## 🧭 Navigation Guide

### For New Developers

#### Where to Start?
1. **Understanding the Domain**: Read this documentation's [Project Overview](#project-overview)
2. **Database Schema**: Review [Database Models](#database-models)
3. **API Contracts**: Check [API Endpoints](#api-endpoints)
4. **Code Entry Points**: 
   - API: `edu/views.py`, `rag_ai/views.py`, `users/views.py`
   - Web: `web/views.py`
   - Models: `*/models.py` in each app

---

### Common Development Tasks

#### Adding a New API Endpoint
```python
# 1. Define view in app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class MyNewView(APIView):
    permission_classes = [IsAuthenticated, SingleDeviceOnly]
    
    def get(self, request):
        # Your logic
        return Response({"message": "success"})

# 2. Add URL in app/urls.py
from .views import MyNewView

urlpatterns = [
    path("api/v1/my-endpoint/", MyNewView.as_view(), name="my_endpoint"),
]

# 3. Test with curl
curl -H "Authorization: Bearer <token>" \
     -H "X-Device-Id: <device>" \
     http://localhost:8000/api/v1/my-endpoint/
```

---

#### Adding a New Model Field
```python
# 1. Edit model in app/models.py
class Lesson(models.Model):
    # existing fields...
    new_field = models.CharField(max_length=100, blank=True)

# 2. Create migration
python manage.py makemigrations

# 3. Review migration file in app/migrations/

# 4. Apply migration
python manage.py migrate

# 5. Update serializer if needed (app/serializers.py)
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'new_field', ...]
```

---

#### Modifying Access Control
```python
# Edit edu/policy.py

PLAN_POLICIES = {
    "basic": {
        "ai_daily_limit": 10,
        "sources": {"qbank"},
        "max_flashcards": 50  # NEW
    },
    # ...
}

def can_create_flashcard(user: User) -> bool:
    policy = get_policy(user)
    count = FlashCard.objects.filter(owner=user).count()
    return count < policy.get("max_flashcards", 0)
```

---

#### Adding a Custom Admin Action
```python
# Edit app/admin.py
from django.contrib import admin

@admin.action(description="Mark selected modules as ready")
def mark_ready(modeladmin, request, queryset):
    queryset.update(is_ready=True)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'semester', 'is_ready']
    actions = [mark_ready]

admin.site.register(Module, ModuleAdmin)
```

---

### File Organization Tips

#### Where to Find Things?

**Feature: User Authentication**
- Models: `users/models.py` → `User`
- Views: `users/views.py` → `register`, `login_with_device`
- URLs: `users/urls.py`
- Permissions: `users/permissions.py` → `SingleDeviceOnly`

**Feature: Question Bank**
- Models: `edu/models.py` → `Question`, `QuestionOption`
- Views: `edu/views.py` → `StudentQuestions`, `StudentQuestionDetail`
- Access Control: `edu/policy.py` → `sources_allowed()`
- Admin: `edu/admin.py` → `QuestionAdmin`

**Feature: AI Chat**
- Models: `rag_ai/models.py` → `Chunk`, `DailyAIUsage`
- Core Logic: `rag_ai/qa.py` → `ask()`, `search_top_k()`
- Views: `rag_ai/views.py` → `AskApiV1`
- Utils: `rag_ai/utils.py` → `can_consume_ai()`

**Feature: Flashcards**
- Model: `edu/models.py` → `FlashCard`
- API Views: `edu/views.py` → `FlashCardListCreate`, `FlashCardDetail`
- Web Views: `web/views.py` → `web_flashcards_panel`, `web_flashcard_create`
- Templates: `templates/components/` → flashcard-related

**Feature: Progress Tracking**
- Models: `edu/models.py` → `LessonProgress`, `StudySession`, `QuestionAttempt`
- Streak Logic: `users/streak.py` → `record_activity()`
- Views: `edu/views.py` → `LessonMarkDoneView`, `QuestionAttemptCreate`

---

### Code Reading Order (for Understanding)

**For API Developers**:
1. `medical_project/settings.py` (configuration)
2. `medical_project/urls.py` (routing)
3. `users/models.py` (user structure)
4. `edu/models.py` (content structure)
5. `edu/views.py` (business logic)
6. `edu/serializers.py` (data transformation)

**For RAG/AI Developers**:
1. `rag_ai/models.py` (data storage)
2. `rag_ai/qa.py` (core algorithms)
3. `rag_ai/views.py` (API interface)
4. `rag_ai/utils.py` (usage tracking)

**For Frontend Developers**:
1. `web/urls.py` (web routes)
2. `web/views.py` (view logic)
3. `templates/base.html` (layout)
4. `templates/pages/` (individual pages)
5. `templates/components/` (reusable UI)

---

## 🔄 Development Workflow

### Typical Development Cycle

```bash
# 1. Create feature branch
git checkout -b feature/new-study-timer

# 2. Make changes
# Edit models, views, templates...

# 3. Create migrations (if models changed)
python manage.py makemigrations
python manage.py migrate

# 4. Run tests (if available)
python manage.py test

# 5. Run development server
python manage.py runserver

# 6. Test manually
# Use Postman/curl for API
# Use browser for web interface

# 7. Commit changes
git add .
git commit -m "Add study timer feature"

# 8. Push and create PR
git push origin feature/new-study-timer
```

---

### Testing API Endpoints

**Using curl**:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123","device_id":"test-device"}'

# Save token
export TOKEN="eyJ0eXAi..."

# Test authenticated endpoint
curl -X GET http://localhost:8000/api/v1/edu/lessons/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Device-Id: test-device"
```

**Using Postman**:
1. Create collection "Medical AI"
2. Add environment variables: `base_url`, `token`, `device_id`
3. Import endpoints from [API Endpoints](#api-endpoints)
4. Add pre-request script to set headers

---

### Database Queries for Debugging

```python
# Django shell
python manage.py shell

# Get user's accessible modules
from users.models import User
from edu.models import Module
user = User.objects.get(username='testuser')
modules = Module.objects.filter(
    semester__year__code=user.study_year,
    is_ready=True
)

# Check AI usage
from rag_ai.models import DailyAIUsage
from datetime import date
usage = DailyAIUsage.objects.get_or_create(user=user, date=date.today())
print(f"AI queries today: {usage[0].count}")

# View user's progress
from edu.models import LessonProgress
progress = LessonProgress.objects.filter(user=user, is_done=True).count()
print(f"Lessons completed: {progress}")

# Check subscription status
print(f"Plan: {user.plan}")
print(f"Active: {user.is_active_subscription}")
print(f"Expires: {user.expires_at}")
```

---

### Common Gotchas & Solutions

#### Problem: pgvector not found
```bash
# Solution: Install extension in PostgreSQL
psql -U postgres -d medical_db
CREATE EXTENSION vector;
```

#### Problem: Migrations conflict
```bash
# Solution: Merge migrations
python manage.py makemigrations --merge
```

#### Problem: Static files not loading
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

#### Problem: JWT token expired
```python
# Solution: Refresh token
POST /api/auth/refresh/
{
  "refresh": "your-refresh-token"
}
```

#### Problem: Device limit reached
```python
# Solution: Admin can reset devices
user = User.objects.get(username='student')
user.device_id_1 = None
user.device_id_2 = None
user.active_device_id = None
user.save()
```

---

## 📝 Additional Notes

### Security Considerations
- Always use HTTPS in production (`SECURE_SSL_REDIRECT=True`)
- Keep `SECRET_KEY` secret (never commit to git)
- Rotate API keys regularly
- Use environment variables for sensitive data
- Implement rate limiting for public endpoints
- Validate file uploads (size, type)

### Performance Optimization
- **Database**: Add indexes on frequently queried fields
- **Caching**: Use Django cache framework for expensive queries
- **Pagination**: Implement on large list endpoints
- **Lazy Loading**: Use `select_related()` and `prefetch_related()`
- **Vector Search**: Tune `ivfflat.probes` parameter

### Monitoring & Logging
- Set up error tracking (Sentry, Rollbar)
- Log AI usage and costs
- Monitor database query performance
- Track API response times
- Set up alerts for subscription expirations

### Backup Strategy
- Daily PostgreSQL backups
- GCS bucket versioning enabled
- Export user data monthly
- Keep migration history

---

## 📚 Useful Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### PostgreSQL & pgvector
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector Django Integration](https://github.com/pgvector/pgvector-python)

### Google AI
- [Gemini API Docs](https://ai.google.dev/docs)
- [Text Embeddings Guide](https://ai.google.dev/docs/embeddings_guide)

### Google Cloud
- [GCS Python Client](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)

---

## 🎯 Quick Command Reference

```bash
# Development
python manage.py runserver                  # Start dev server
python manage.py shell                      # Django shell
python manage.py dbshell                    # Database shell

# Database
python manage.py makemigrations             # Create migrations
python manage.py migrate                    # Apply migrations
python manage.py showmigrations             # List migrations

# User Management
python manage.py createsuperuser            # Create admin
python manage.py changepassword <username>  # Change password

# Static Files
python manage.py collectstatic              # Collect static files
python manage.py findstatic <file>          # Find static file location

# Testing
python manage.py test                       # Run tests
python manage.py test app.tests.TestClass   # Run specific test

# Production
gunicorn medical_project.wsgi:application   # Run with gunicorn
```

---

## 📧 Support & Contact

For questions or issues with this codebase, consult:
1. This documentation
2. Inline code comments
3. Django/DRF documentation
4. PostgreSQL and pgvector docs

---

**Last Updated**: December 24, 2025
**Version**: 1.0
**Maintainer**: Medical AI Team
