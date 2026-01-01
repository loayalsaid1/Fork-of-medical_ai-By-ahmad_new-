# System Architecture & Data Flow Diagrams

## 📊 Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│                                                                 │
│  ┌─────────────────────┐           ┌─────────────────────┐    │
│  │   Mobile App        │           │   Web Browser       │    │
│  │  (iOS/Android)      │           │   (HTML/JS/CSS)     │    │
│  │                     │           │                     │    │
│  │  - REST API calls   │           │  - Django templates │    │
│  │  - JWT auth         │           │  - Session auth     │    │
│  │  - JSON responses   │           │  - HTMX/forms       │    │
│  └──────────┬──────────┘           └──────────┬──────────┘    │
└─────────────┼─────────────────────────────────┼────────────────┘
              │                                 │
              │ Authorization: Bearer TOKEN     │ Cookie: sessionid
              │ X-Device-Id: device-uuid        │
              ▼                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
│                         (Django 5.2)                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                    URL Router                           │   │
│  │  medical_project/urls.py                               │   │
│  │  ├─ /api/auth/*     → users.urls                       │   │
│  │  ├─ /api/v1/edu/*   → edu.urls                         │   │
│  │  ├─ /api/v1/ask/*   → rag_ai.urls                      │   │
│  │  ├─ /admin/*        → django.contrib.admin             │   │
│  │  └─ /*              → web.urls                          │   │
│  └────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              MIDDLEWARE PIPELINE                          │ │
│  │  1. Security                                             │ │
│  │  2. Session                                              │ │
│  │  3. CSRF                                                 │ │
│  │  4. Authentication (JWT/Session)                         │ │
│  │  5. SingleDeviceOnly Permission                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │   EDU APP     │  │  RAG_AI APP   │  │  USERS APP    │     │
│  │               │  │               │  │               │     │
│  │ • Content     │  │ • AI Chat     │  │ • Auth        │     │
│  │ • Questions   │  │ • Vectors     │  │ • Plans       │     │
│  │ • Progress    │  │ • RAG         │  │ • Payments    │     │
│  │ • Flashcards  │  │ • Usage       │  │ • Streaks     │     │
│  │               │  │               │  │               │     │
│  │ Views         │  │ Views         │  │ Views         │     │
│  │ Serializers   │  │ QA Logic      │  │ Serializers   │     │
│  │ Policy        │  │ Utils         │  │ Permissions   │     │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘     │
└──────────┼──────────────────┼──────────────────┼──────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            PostgreSQL 14+ with pgvector                  │  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │  edu_*      │  │  rag_ai_*    │  │  users_*     │  │  │
│  │  │  tables     │  │  tables      │  │  tables      │  │  │
│  │  │             │  │              │  │              │  │  │
│  │  │ • year      │  │ • chunk      │  │ • user       │  │  │
│  │  │ • semester  │  │   - content  │  │ • plan       │  │  │
│  │  │ • module    │  │   - vector   │  │ • coupon     │  │  │
│  │  │ • subject   │  │   (768-dim)  │  │ • streak     │  │  │
│  │  │ • lesson    │  │              │  │ • payment    │  │  │
│  │  │ • question  │  │ • usage      │  │              │  │  │
│  │  │ • flashcard │  │   - daily    │  │              │  │  │
│  │  │ • progress  │  │   - limits   │  │              │  │  │
│  │  └─────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                          │  │
│  │  Indexes:                                                │  │
│  │  • IVFFlat index on embedding_vec (vector search)       │  │
│  │  • B-tree indexes on FKs, dates, study_year             │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                           │
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  Google AI (Gemini)  │         │ Google Cloud Storage │    │
│  │                      │         │                      │    │
│  │  • Embeddings        │         │  • PDFs              │    │
│  │    (text-embedding)  │         │  • Images            │    │
│  │  • Text Generation   │         │  • Media files       │    │
│  │    (gemini-flash)    │         │                      │    │
│  └──────────────────────┘         └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Diagrams

### 1. Authentication Flow (Mobile App)

```
┌─────────┐                                                    ┌─────────┐
│ Mobile  │                                                    │ Django  │
│   App   │                                                    │  API    │
└────┬────┘                                                    └────┬────┘
     │                                                              │
     │  POST /api/auth/register/                                   │
     │  {"username", "password", "study_year"}                     │
     ├────────────────────────────────────────────────────────────>│
     │                                                              │
     │                                         [Create User]        │
     │                                         [Hash password]      │
     │                                                              │
     │  {"id", "username", "study_year"}                           │
     │<────────────────────────────────────────────────────────────┤
     │                                                              │
     │                                                              │
     │  POST /api/auth/login/                                      │
     │  {"username", "password", "device_id"}                      │
     ├────────────────────────────────────────────────────────────>│
     │                                                              │
     │                                         [Validate creds]     │
     │                                         [Check device_id]    │
     │                                         [Generate JWT]       │
     │                                                              │
     │  {"access": "JWT...", "refresh": "JWT..."}                  │
     │<────────────────────────────────────────────────────────────┤
     │                                                              │
     │                                                              │
     │  GET /api/v1/edu/lessons/                                   │
     │  Headers:                                                   │
     │    Authorization: Bearer JWT...                             │
     │    X-Device-Id: device-uuid                                 │
     ├────────────────────────────────────────────────────────────>│
     │                                                              │
     │                              [Verify JWT]                   │
     │                              [Check device_id matches]      │
     │                              [Check subscription active]    │
     │                              [Query lessons]                │
     │                                                              │
     │  [{"id": 1, "title": "...", ...}, ...]                      │
     │<────────────────────────────────────────────────────────────┤
     │                                                              │
```

---

### 2. RAG (AI Chat) Flow

```
┌──────┐          ┌───────┐          ┌──────────┐          ┌────────┐
│ User │          │ API   │          │ RAG      │          │Google  │
│      │          │ View  │          │ qa.py    │          │Gemini  │
└──┬───┘          └───┬───┘          └────┬─────┘          └───┬────┘
   │                  │                   │                    │
   │ POST /api/v1/ask/│                   │                    │
   │ {"q": "What is   │                   │                    │
   │  diabetes?"}     │                   │                    │
   ├─────────────────>│                   │                    │
   │                  │                   │                    │
   │                  │ [Check daily      │                    │
   │                  │  AI usage limit]  │                    │
   │                  │                   │                    │
   │                  │ ask(question)     │                    │
   │                  ├──────────────────>│                    │
   │                  │                   │                    │
   │                  │                   │ embed_query()      │
   │                  │                   ├───────────────────>│
   │                  │                   │                    │
   │                  │                   │  [768-dim vector]  │
   │                  │                   │<───────────────────┤
   │                  │                   │                    │
   │                  │       [PostgreSQL pgvector search]     │
   │                  │       SELECT * FROM rag_ai_chunk       │
   │                  │       ORDER BY embedding_vec <=>       │
   │                  │       '[0.1, 0.2, ...]' LIMIT 15       │
   │                  │                   │                    │
   │                  │       [Get top K chunks]               │
   │                  │                   │                    │
   │                  │                   │ [Build context     │
   │                  │                   │  from chunks]      │
   │                  │                   │                    │
   │                  │                   │ generate_answer()  │
   │                  │                   ├───────────────────>│
   │                  │                   │  Context + Query   │
   │                  │                   │                    │
   │                  │                   │  [Generated answer]│
   │                  │                   │<───────────────────┤
   │                  │                   │                    │
   │                  │ {"answer": "...", │                    │
   │                  │  "sources": [...]}│                    │
   │                  │<──────────────────┤                    │
   │                  │                   │                    │
   │                  │ [Update usage     │                    │
   │                  │  counter]         │                    │
   │                  │                   │                    │
   │ Response         │                   │                    │
   │<─────────────────┤                   │                    │
   │                  │                   │                    │
```

**Detailed RAG Steps**:

1. **Input**: User question "What is diabetes?"
2. **Embedding**: Convert question → 768-dimensional vector using Gemini
3. **Vector Search**: 
   ```sql
   SELECT id, content, (embedding_vec <=> query_vec) AS distance
   FROM rag_ai_chunk
   ORDER BY distance ASC
   LIMIT 15
   ```
4. **Context Building**: Concatenate top K chunk texts
5. **Prompt Engineering**:
   ```
   You are a medical AI assistant.
   
   Context from medical textbooks:
   [chunk1 content]
   [chunk2 content]
   ...
   
   Question: What is diabetes?
   
   Answer:
   ```
6. **LLM Generation**: Send to Gemini → get answer
7. **Response**: Return answer + source citations

---

### 3. Content Access Control Flow

```
┌──────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│ User │     │  View   │     │ Policy  │     │  Model   │
└──┬───┘     └────┬────┘     └────┬────┘     └────┬─────┘
   │              │               │               │
   │ GET /lessons │               │               │
   ├─────────────>│               │               │
   │              │               │               │
   │              │ [Get user     │               │
   │              │  from JWT]    │               │
   │              │               │               │
   │              │ can_view_     │               │
   │              │ lesson(user)  │               │
   │              ├──────────────>│               │
   │              │               │               │
   │              │               │ [Check        │
   │              │               │  is_active_   │
   │              │               │  subscription]│
   │              │               │               │
   │              │               │ [Get policy   │
   │              │               │  for plan]    │
   │              │               │               │
   │              │ True/False    │               │
   │              │<──────────────┤               │
   │              │               │               │
   │              │ Lesson.objects│               │
   │              │  .filter(     │               │
   │              │   subject__   │               │
   │              │   module__    │               │
   │              │   semester__  │               │
   │              │   year__code= │               │
   │              │   user.study_ │               │
   │              │   year,       │               │
   │              │   module__    │               │
   │              │   is_ready=   │               │
   │              │   True)       │               │
   │              ├──────────────────────────────>│
   │              │               │               │
   │              │               │  [QuerySet]   │
   │              │<──────────────────────────────┤
   │              │               │               │
   │  [Lessons]   │               │               │
   │<─────────────┤               │               │
   │              │               │               │
```

**Access Control Rules**:
- User must have `is_active_subscription = True`
- Content filtered by `user.study_year`
- Modules must have `is_ready = True`
- Questions filtered by plan's allowed sources
- Flashcards filtered by plan (admin vs user-created)
- AI queries limited by daily quota

---

### 4. Subscription Purchase Flow

```
┌──────┐          ┌─────────┐          ┌─────────┐
│ User │          │  API    │          │Database │
└──┬───┘          └────┬────┘          └────┬────┘
   │                   │                    │
   │ GET /plans/       │                    │
   ├──────────────────>│                    │
   │                   │ Plan.objects.all() │
   │                   ├───────────────────>│
   │                   │                    │
   │                   │   [Plans list]     │
   │                   │<───────────────────┤
   │  [Plans]          │                    │
   │<──────────────────┤                    │
   │                   │                    │
   │ POST /coupons/    │                    │
   │   validate/       │                    │
   │ {"code": "SAVE20"}│                    │
   ├──────────────────>│                    │
   │                   │ Coupon.objects.get │
   │                   ├───────────────────>│
   │                   │                    │
   │                   │ [Check validity]   │
   │                   │ [Check usage]      │
   │                   │                    │
   │  {"percent": 20,  │                    │
   │   "final_price":  │                    │
   │   159.20}         │                    │
   │<──────────────────┤                    │
   │                   │                    │
   │ POST /           │                    │
   │  subscriptions/   │                    │
   │  purchase/        │                    │
   │ {"plan_id": 1,    │                    │
   │  "coupon": "..."}│                    │
   ├──────────────────>│                    │
   │                   │                    │
   │                   │ [Validate payment] │
   │                   │                    │
   │                   │ Payment.create()   │
   │                   ├───────────────────>│
   │                   │                    │
   │                   │ User.update(       │
   │                   │   plan='basic',    │
   │                   │   is_active=True,  │
   │                   │   expires_at=...)  │
   │                   ├───────────────────>│
   │                   │                    │
   │                   │ Coupon.update(     │
   │                   │   used_count+=1)   │
   │                   ├───────────────────>│
   │                   │                    │
   │  {"status": "ok", │                    │
   │   "expires_at":   │                    │
   │   "2026-12-24"}   │                    │
   │<──────────────────┤                    │
   │                   │                    │
```

---

### 5. Progress Tracking Flow

```
┌──────┐          ┌─────────┐          ┌─────────┐
│ User │          │  View   │          │Database │
└──┬───┘          └────┬────┘          └────┬────┘
   │                   │                    │
   │ [User reads       │                    │
   │  lesson]          │                    │
   │                   │                    │
   │ POST /lessons/5/  │                    │
   │      progress/    │                    │
   │      done/        │                    │
   ├──────────────────>│                    │
   │                   │                    │
   │                   │ record_activity()  │
   │                   │  [Update streak]   │
   │                   ├───────────────────>│
   │                   │  UserStreak.update │
   │                   │                    │
   │                   │ LessonProgress     │
   │                   │  .update_or_create │
   │                   ├───────────────────>│
   │                   │  (user, lesson,    │
   │                   │   is_done=True)    │
   │                   │                    │
   │  {"status": "ok"} │                    │
   │<──────────────────┤                    │
   │                   │                    │
   │                   │                    │
   │ [Later: check     │                    │
   │  dashboard]       │                    │
   │                   │                    │
   │ GET /home-        │                    │
   │     dashboard/    │                    │
   ├──────────────────>│                    │
   │                   │                    │
   │                   │ UserStreak.get()   │
   │                   ├───────────────────>│
   │                   │  current_streak    │
   │                   │                    │
   │                   │ LessonProgress     │
   │                   │  .filter().count() │
   │                   ├───────────────────>│
   │                   │  completed_count   │
   │                   │                    │
   │                   │ QuestionAttempt    │
   │                   │  .filter().count() │
   │                   ├───────────────────>│
   │                   │  questions_solved  │
   │                   │                    │
   │  {"streak": 7,    │                    │
   │   "lessons": 42,  │                    │
   │   "questions": 156│                    │
   │  }                │                    │
   │<──────────────────┤                    │
   │                   │                    │
```

---

## 🗃️ Data Model Relationships

```
┌──────────────────────────────────────────────────────────────────┐
│                    CONTENT HIERARCHY                             │
└──────────────────────────────────────────────────────────────────┘

Year (y1-y5)
  │
  │ 1:N
  ▼
Semester
  │
  │ 1:N
  ▼
Module (is_ready flag)
  │
  │ 1:N
  ▼
Subject
  │
  │ 1:N
  ▼
Chapter (optional)
  │
  │ 1:N
  ▼
Lesson (content, PDF)
  │
  ├─────────────┬────────────────┐
  │ 1:N         │ 1:N            │ 1:N
  ▼             ▼                ▼
Question    FlashCard    LessonProgress
  │             │                │
  │ 1:N         │                │ N:1
  ▼             │                ▼
QuestionOption  │              User
  │             │                │
  │ 1:N         │ N:1            │ 1:N
  ▼             ▼                ▼
QuestionAttempt                UserStreak
  │                              (1:1 with User)
  │ N:1
  ▼
StudySession


┌──────────────────────────────────────────────────────────────────┐
│                    USER & SUBSCRIPTIONS                          │
└──────────────────────────────────────────────────────────────────┘

User (AbstractUser + custom fields)
  │
  ├─── plan (CharField: none/basic/premium/advanced)
  ├─── is_active_subscription (Boolean)
  ├─── expires_at (DateTime)
  ├─── device_id_1, device_id_2 (device binding)
  │
  │ 1:N
  ├──────> Payment
  │
  │ 1:1
  ├──────> UserStreak
  │
  │ 1:N
  ├──────> LessonProgress
  │
  │ 1:N
  ├──────> FlashCard (owner_type='user')
  │
  │ 1:N
  ├──────> FavoriteLesson
  │
  │ 1:N
  ├──────> PlannerTask
  │
  │ 1:N
  ├──────> StudySession
  │
  │ 1:N
  └──────> DailyAIUsage

Plan (pricing tiers)
  │ 1:N
  └──────> Payment

Coupon (discount codes)
  │ N:N (tracked in Payment)
  └──────> Payment


┌──────────────────────────────────────────────────────────────────┐
│                    RAG / AI SYSTEM                               │
└──────────────────────────────────────────────────────────────────┘

Chunk
  │
  ├─── file_name (source PDF)
  ├─── chunk_index (position in file)
  ├─── content (actual text)
  └─── embedding_vec (vector[768])
       │
       └─── IVFFlat Index (for fast similarity search)

DailyAIUsage
  │ N:1
  ├──────> User
  ├─── date
  └─── count (number of queries that day)
```

---

## 🔐 Security Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION LAYERS                         │
└──────────────────────────────────────────────────────────────────┘

Layer 1: Transport Security
  ├─ HTTPS (TLS 1.2+)
  ├─ SECURE_SSL_REDIRECT=True
  ├─ SESSION_COOKIE_SECURE=True
  └─ CSRF_COOKIE_SECURE=True

Layer 2: Authentication
  ├─ JWT (for API)
  │  ├─ Access Token (2 days)
  │  ├─ Refresh Token (7 days)
  │  └─ HS256 signing
  └─ Session (for Web)
     └─ Django session middleware

Layer 3: Device Binding
  ├─ X-Device-Id header required
  ├─ User can register max 2 devices
  ├─ Only 1 device active at a time
  └─ SingleDeviceOnly permission checks

Layer 4: Authorization
  ├─ Subscription status check
  │  └─ is_active_subscription must be True
  ├─ Plan-based access control
  │  ├─ Questions filtered by allowed sources
  │  ├─ AI queries limited by daily quota
  │  └─ Flashcard visibility by plan
  └─ Content visibility
     ├─ Filtered by user.study_year
     └─ Modules must be is_ready=True

Layer 5: Rate Limiting
  ├─ AI queries: daily limit per plan
  ├─ Question reveals: tracked per user
  └─ API throttling (can be added)

Layer 6: Data Security
  ├─ Password hashing (Django's PBKDF2)
  ├─ Environment variables for secrets
  ├─ SQL injection prevention (ORM)
  └─ XSS prevention (template escaping)
```

---

## 📈 Performance Optimization Strategy

```
┌──────────────────────────────────────────────────────────────────┐
│                    DATABASE OPTIMIZATION                         │
└──────────────────────────────────────────────────────────────────┘

1. Indexes
   ├─ B-tree indexes on:
   │  ├─ Foreign keys
   │  ├─ user.study_year
   │  ├─ module.is_ready
   │  ├─ dates (created_at, due_date, etc.)
   │  └─ device_id fields
   │
   └─ Vector index:
      └─ IVFFlat on rag_ai_chunk.embedding_vec
         └─ Tunable with SET ivfflat.probes

2. Query Optimization
   ├─ select_related() for 1:1 and N:1
   ├─ prefetch_related() for N:N and 1:N
   ├─ .only() for specific fields
   └─ .count() instead of len(queryset)

3. Connection Pooling
   └─ PostgreSQL connection pooling

4. Pagination
   ├─ Large lists paginated
   └─ DRF pagination classes


┌──────────────────────────────────────────────────────────────────┐
│                    CACHING STRATEGY                              │
└──────────────────────────────────────────────────────────────────┘

1. Static Files
   └─ WhiteNoise compression + caching headers

2. Database Query Cache (can be added)
   ├─ Redis/Memcached
   ├─ Cache plan policies
   ├─ Cache user permissions
   └─ Cache frequently accessed content

3. Vector Search Cache (can be added)
   └─ Cache embedding vectors for common queries


┌──────────────────────────────────────────────────────────────────┐
│                    AI/RAG OPTIMIZATION                           │
└──────────────────────────────────────────────────────────────────┘

1. Vector Search Tuning
   ├─ IVFFlat lists parameter
   │  └─ Optimal: sqrt(total_rows)
   ├─ Probes parameter
   │  └─ Higher = more accurate, slower
   └─ Distance metric: cosine

2. Context Limiting
   ├─ max_chars parameter
   ├─ Top K chunks selection
   └─ Avoid token limit overflow

3. Batch Processing (for ingestion)
   └─ Chunk and embed in batches
```

---

## 🚀 Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                              │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│   Load Balancer     │  (Heroku/Railway/Nginx)
│   - HTTPS           │
│   - SSL Termination │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Gunicorn          │  (WSGI Server)
│   - Workers: 4      │
│   - Threads: 2      │
│   - Timeout: 60s    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Django App        │
│   - DEBUG=False     │
│   - ALLOWED_HOSTS   │
│   - SSL enforced    │
└──────────┬──────────┘
           │
           ├──────────────────┐
           │                  │
           ▼                  ▼
┌──────────────────┐  ┌───────────────┐
│   PostgreSQL     │  │  Google Cloud │
│   - Managed DB   │  │               │
│   - Backups      │  ├─ GCS Storage  │
│   - pgvector     │  └─ Gemini API   │
└──────────────────┘  └───────────────┘


Environment Variables (Production):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://...
GOOGLE_API_KEY=...
GCS_CREDENTIALS_JSON={...}
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 📊 Monitoring & Observability

```
┌──────────────────────────────────────────────────────────────────┐
│                    LOGGING STRATEGY                              │
└──────────────────────────────────────────────────────────────────┘

Application Logs
  ├─ Error tracking (Sentry/Rollbar)
  ├─ API request logs
  ├─ Authentication failures
  └─ Business logic errors

AI/RAG Logs
  ├─ Query latency
  ├─ Token usage
  ├─ Embedding errors
  └─ Daily usage by user

Database Logs
  ├─ Slow queries (>1s)
  ├─ Connection errors
  └─ Migration history

Security Logs
  ├─ Failed login attempts
  ├─ Device binding violations
  └─ Unauthorized access attempts


┌──────────────────────────────────────────────────────────────────┐
│                    METRICS TO TRACK                              │
└──────────────────────────────────────────────────────────────────┘

Performance
  ├─ API response time (p50, p95, p99)
  ├─ Database query time
  ├─ Vector search latency
  └─ Page load time

Usage
  ├─ Daily active users
  ├─ Lessons completed
  ├─ Questions attempted
  ├─ AI queries per day
  └─ Subscription renewals

Business
  ├─ New registrations
  ├─ Trial conversions
  ├─ Revenue (by plan)
  └─ Churn rate

System Health
  ├─ CPU/Memory usage
  ├─ Database connections
  ├─ Storage usage (GCS)
  └─ Error rate
```

---

This comprehensive diagram set covers all major architectural aspects of your medical AI platform!
