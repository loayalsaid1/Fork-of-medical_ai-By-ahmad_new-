# 🧭 Quick Navigation Guide

> **A fast reference for navigating the medical_ai codebase**

## 📍 "I want to..."

### Work with User Authentication
```
├── User Model: users/models.py (line 12-64)
├── Login API: users/views.py → login_with_device()
├── Register API: users/views.py → register()
├── JWT Config: medical_project/settings.py → SIMPLE_JWT
└── Device Permission: users/permissions.py → SingleDeviceOnly
```

### Work with Educational Content (Lessons, Modules, etc.)
```
├── Models: edu/models.py
│   ├── Year (line 5)
│   ├── Semester (line 36)
│   ├── Module (line 49)
│   ├── Subject (line 66)
│   ├── Chapter (line 81)
│   └── Lesson (line 95+)
├── API Views: edu/views.py
│   ├── YearMe (line 45)
│   ├── StudentSemesters (line 51)
│   ├── StudentModules (line 57)
│   ├── StudentSubjects (line 69)
│   ├── StudentChapters (line 84)
│   └── StudentLessons (line 100+)
└── URLs: edu/urls.py
```

### Work with Questions
```
├── Question Model: edu/models.py → Question class
├── QuestionOption Model: edu/models.py → QuestionOption class
├── List API: edu/views.py → StudentQuestions
├── Detail API: edu/views.py → StudentQuestionDetail
├── Access Control: edu/policy.py → sources_allowed()
├── Web Browse: web/views.py → web_questions_browse()
└── Templates: templates/pages/ → questions-related
```

### Work with AI Chat (RAG System)
```
├── Chunk Model: rag_ai/models.py → Chunk
├── Core Algorithm: rag_ai/qa.py
│   ├── embed_query() - Convert text to vectors
│   ├── search_top_k() - pgvector similarity search
│   └── ask() - Full RAG pipeline
├── API Endpoint: rag_ai/views.py → AskApiV1
├── Usage Tracking: rag_ai/utils.py → can_consume_ai()
└── Usage Model: rag_ai/models.py → DailyAIUsage
```

### Work with Flashcards
```
├── Model: edu/models.py → FlashCard
├── API Views: edu/views.py
│   ├── FlashCardListCreate
│   └── FlashCardDetail
├── Web Views: web/views.py
│   ├── web_flashcards_panel()
│   ├── web_flashcard_create()
│   ├── web_flashcard_update()
│   └── web_flashcard_delete()
└── Policy: edu/policy.py → flashcard_visibility_q()
```

### Work with Subscriptions & Plans
```
├── Models: users/models.py
│   ├── Plan (line 55)
│   ├── Coupon (line 64)
│   └── Payment (later in file)
├── Views: users/views.py
│   ├── PlanListView
│   ├── StartFreeTrialView
│   ├── PurchaseSubscriptionView
│   └── CouponValidateView
└── Access Control: edu/policy.py → PLAN_POLICIES
```

### Work with Progress Tracking
```
├── Models: edu/models.py
│   ├── LessonProgress
│   ├── StudySession
│   └── QuestionAttempt
├── Streak Logic: users/streak.py → record_activity()
├── API Views: edu/views.py
│   ├── LessonMarkDoneView
│   ├── QuestionAttemptCreate
│   └── StudySessionListCreate
└── Dashboard: edu/views.py → HomeDashboardView
```

### Work with Web Interface (HTML)
```
├── URLs: web/urls.py (complete routing map)
├── Views: web/views.py (2387 lines)
│   ├── Landing: landing_page()
│   ├── Auth: login_view(), register_view()
│   ├── Materials: materials_home(), materials_lesson()
│   └── Questions: web_questions_browse()
├── Templates: templates/
│   ├── Base: base.html
│   ├── Pages: pages/
│   ├── Components: components/
│   └── Partials: _partials/
└── Static: static/ (CSS, JS, images)
```

---

## 🔍 "I need to understand..."

### How API Authentication Works
1. **Login**: `POST /api/auth/login/` with username, password, device_id
2. **Get Tokens**: Returns `access` (JWT) and `refresh` tokens
3. **Use Token**: Add header `Authorization: Bearer <access>`
4. **Device Binding**: Add header `X-Device-Id: <device-id>`
5. **Refresh**: `POST /api/auth/refresh/` with refresh token when access expires

**Code Flow**:
```
users/views.py → login_with_device()
   ↓
medical_project/settings.py → SIMPLE_JWT config
   ↓
users/permissions.py → SingleDeviceOnly checks device_id
```

---

### How Vector Search Works (RAG)
1. **Ingestion**: PDFs → chunked → embedded → stored in `rag_ai_chunk` table
2. **Query**: User question → `embed_query()` → 768-dim vector
3. **Search**: pgvector IVFFlat index → cosine similarity → top K chunks
4. **Generation**: Chunks as context → Gemini LLM → answer

**Code Flow**:
```
rag_ai/views.py → AskApiV1.post()
   ↓
rag_ai/qa.py → ask()
   ├── embed_query() - Google Gemini embedding
   ├── search_top_k() - pgvector SQL query
   └── (LLM generation with context)
```

**Database**:
```sql
-- Table: rag_ai_chunk
embedding_vec vector(768)  -- pgvector column
-- Index: IVFFlat for fast approximate search
```

---

### How Access Control Works
**Plan-Based**:
```python
# edu/policy.py
PLAN_POLICIES = {
    "none":     {"ai_daily_limit": 0,   "sources": set()},
    "basic":    {"ai_daily_limit": 10,  "sources": {"qbank"}},
    "premium":  {"ai_daily_limit": 30,  "sources": {"qbank", "exam_review"}},
    "advanced": {"ai_daily_limit": 100, "sources": {"all types"}},
}
```

**Enforcement Points**:
- Questions: `edu/views.py` → checks `can_view_questions(user)`
- AI Chat: `rag_ai/utils.py` → checks daily limit via `DailyAIUsage`
- Flashcards: `edu/views.py` → filters by `flashcard_visibility_q(user)`
- Content: `edu/views.py` → filters by `user.study_year`

---

### How Content Hierarchy Works
```
Year (y1-y5)
   └── Semester (1st, 2nd)
       └── Module (Cardiovascular, Respiratory, etc.)
           └── Subject (Anatomy, Physiology, Pathology, etc.)
               └── Chapter (optional grouping)
                   └── Lesson (actual content with PDF)
                       ├── Questions (linked)
                       └── FlashCards (linked)
```

**Filtering in API**:
```python
# User with study_year='y3' only sees Year 3 content
modules = Module.objects.filter(
    semester__year__code='y3',
    is_ready=True  # Admin control
)
```

**Code**: `edu/models.py` (lines 5-95)

---

### How Subscriptions Work
**States**:
```
User.plan: 'none' | 'basic' | 'premium' | 'advanced'
User.is_active_subscription: True/False
User.expires_at: DateTime
```

**Activation Flow**:
```
1. Purchase → users/views.py → PurchaseSubscriptionView
2. Validate payment
3. Set is_active_subscription = True
4. Set activated_at = now
5. Set expires_at = now + plan.duration_days
6. Update user.plan
```

**Coupon Application**:
```python
# users/views.py → PurchaseSubscriptionView
final_price = plan.price_egp * (1 - coupon.percent / 100)
```

---

## 🗺️ Directory Map

```
medical_ai/
│
├── 🔧 Config
│   ├── medical_project/settings.py    # Django settings, apps, DB, storage
│   ├── medical_project/urls.py        # Root URL routing
│   └── .env                           # Environment variables (CREATE THIS)
│
├── 🎓 EDU (Education)
│   ├── models.py ⭐                   # All educational models (434 lines)
│   ├── views.py ⭐                    # 40+ API views (1447 lines)
│   ├── serializers.py                 # DRF serializers
│   ├── urls.py                        # API routing (70+ endpoints)
│   ├── policy.py                      # Access control logic
│   └── admin.py                       # Django admin config
│
├── 🤖 RAG_AI (AI Chat)
│   ├── models.py                      # Chunk, DailyAIUsage
│   ├── qa.py ⭐                       # RAG algorithm (250 lines)
│   ├── views.py                       # AI API endpoints
│   ├── utils.py                       # Usage tracking helpers
│   └── urls.py                        # AI routing
│
├── 👤 USERS (Auth & Subscriptions)
│   ├── models.py ⭐                   # User, Plan, Coupon, Streak (174 lines)
│   ├── views.py                       # Auth, subscription APIs
│   ├── permissions.py                 # SingleDeviceOnly permission
│   ├── streak.py                      # Daily activity tracking
│   └── urls.py                        # Auth routing
│
├── 🌐 WEB (Frontend)
│   ├── views.py ⭐                    # All web pages (2387 lines!)
│   ├── urls.py                        # Web routing (110 lines)
│   └── (uses templates/ for HTML)
│
├── 📄 TEMPLATES
│   ├── base.html                      # Master layout
│   ├── landing_page.html              # Homepage
│   ├── pages/                         # Full pages
│   ├── components/                    # Reusable UI components
│   └── _partials/                     # Header, footer, nav
│
└── 📊 DATABASE
    └── PostgreSQL + pgvector
        ├── edu_* tables               # Educational content
        ├── rag_ai_chunk               # Vector embeddings
        └── users_* tables             # Users, plans, payments

⭐ = Start here for understanding
```

---

## 🚀 Common Tasks Cheat Sheet

### Adding a New API Endpoint
```python
# 1. edu/views.py
class MyView(APIView):
    permission_classes = [IsAuthenticated, SingleDeviceOnly]
    def get(self, request):
        return Response({"data": "..."})

# 2. edu/urls.py
path("api/v1/my-endpoint/", MyView.as_view(), name="my_endpoint"),

# 3. Test
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/my-endpoint/
```

### Adding a Model Field
```bash
# 1. Edit model in app/models.py
# 2. Create migration
python manage.py makemigrations
# 3. Apply
python manage.py migrate
# 4. Update serializer if needed
```

### Checking User Access
```python
# Django shell
python manage.py shell

from users.models import User
from edu.policy import get_policy, sources_allowed

user = User.objects.get(username='student')
print(f"Plan: {user.plan}")
print(f"Policy: {get_policy(user)}")
print(f"Sources: {sources_allowed(user)}")
```

### Debugging Vector Search
```python
from rag_ai.qa import search_top_k

results = search_top_k("What is diabetes?", k=5)
for distance, chunk in results:
    print(f"Distance: {distance:.4f}")
    print(f"File: {chunk.file_name}")
    print(f"Content: {chunk.content[:100]}...")
```

### Resetting User Devices
```python
user = User.objects.get(username='student')
user.device_id_1  = None
user.device_id_2 = None
user.active_device_id = None
user.save()
```

---

## 📖 Reading Order for New Developers

### Day 1: Overview
1. ✅ Read `DOCUMENTATION.md` (full documentation)
2. ✅ Read this `NAVIGATION_GUIDE.md`
3. 📖 Skim `medical_project/settings.py` (understand config)
4. 📖 Skim `medical_project/urls.py` (understand routing)

### Day 2: Core Models
1. 📖 Read `users/models.py` (understand User, Plan)
2. 📖 Read `edu/models.py` (understand content hierarchy)
3. 📖 Read `rag_ai/models.py` (understand Chunk, vector storage)

### Day 3: Business Logic
1. 📖 Read `edu/policy.py` (access control)
2. 📖 Read `users/streak.py` (activity tracking)
3. 📖 Skim `edu/views.py` (main API logic - pick 3-4 views)

### Day 4: AI System
1. 📖 Read `rag_ai/qa.py` (full RAG algorithm)
2. 📖 Read `rag_ai/views.py` (AI API)
3. 📖 Read `rag_ai/utils.py` (usage limits)

### Day 5: Web Interface (if working on frontend)
1. 📖 Read `web/urls.py` (web routing map)
2. 📖 Skim `web/views.py` (pick 3-4 views to understand pattern)
3. 📖 Read `templates/base.html` (layout structure)

---

## 🔗 External Dependencies Quick Links

### Django & DRF
- [Django Models](https://docs.djangoproject.com/en/5.2/topics/db/models/)
- [DRF Views](https://www.django-rest-framework.org/api-guide/views/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)

### PostgreSQL & pgvector
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector Indexes](https://github.com/pgvector/pgvector#indexing)

### Google AI
- [Gemini Quickstart](https://ai.google.dev/tutorials/python_quickstart)
- [Embeddings API](https://ai.google.dev/docs/embeddings_guide)

---

## ❓ FAQ

**Q: Where are the actual lesson PDFs stored?**  
A: Google Cloud Storage (GCS). See `medical_project/settings.py` → `GS_BUCKET_NAME`

**Q: How do I add a new question type?**  
A: Edit `edu/models.py` → `Question.source` choices, then update `edu/policy.py` → `PLAN_POLICIES`

**Q: How do I change AI model?**  
A: Edit `.env` → `GEMINI_GEN_MODEL` and `GEMINI_EMBED_MODEL`

**Q: Where is the admin panel?**  
A: `http://localhost:8000/admin/` (create superuser first)

**Q: How do I test the API without a mobile app?**  
A: Use Postman, curl, or Django REST Framework's browsable API

**Q: Where are migrations stored?**  
A: Each app has a `migrations/` folder: `edu/migrations/`, `users/migrations/`, etc.

---

## 🎯 Key Files Reference

| Task | File | Line/Function |
|------|------|---------------|
| User registration | `users/views.py` | `register()` |
| User login | `users/views.py` | `login_with_device()` |
| Device permission | `users/permissions.py` | `SingleDeviceOnly` |
| Question list | `edu/views.py` | `StudentQuestions` |
| Lesson detail | `edu/views.py` | `LessonDetail` |
| AI chat | `rag_ai/views.py` | `AskApiV1` |
| Vector search | `rag_ai/qa.py` | `search_top_k()` |
| Embedding | `rag_ai/qa.py` | `embed_query()` |
| Access control | `edu/policy.py` | `get_policy()` |
| Streak tracking | `users/streak.py` | `record_activity()` |
| Web landing | `web/views.py` | `landing_page()` |
| Web materials | `web/views.py` | `materials_home()` |

---

**This is your map to the codebase. Bookmark it! 📌**
