"""
Database Seeding Script for Medical AI Platform
Run with: python seed_database.py
"""

import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_project.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from edu.models import (
    Year, Semester, Module, Subject, Chapter, Lesson,
    Question, QuestionOption, FlashCard, FavoriteLesson,
    LessonProgress, PlannerTask, StudySession, QuestionAttempt
)
from users.models import Plan, Coupon, UserStreak

User = get_user_model()

def seed_all():
    print("🌱 Starting database seeding...")
    
    # 1. Create Plans
    print("\n📦 Creating subscription plans...")
    plans = create_plans()
    
    # 2. Update admin user
    print("\n👤 Updating admin user...")
    admin = update_admin_user(plans['premium'])
    
    # 3. Create Years
    print("\n📅 Creating years...")
    years = create_years()
    
    # 4. Create Semesters
    print("\n📚 Creating semesters...")
    semesters = create_semesters(years)
    
    # 5. Create Modules
    print("\n📖 Creating modules...")
    modules = create_modules(semesters)
    
    # 6. Create Subjects
    print("\n🔬 Creating subjects...")
    subjects = create_subjects(modules)
    
    # 7. Create Chapters
    print("\n📑 Creating chapters...")
    chapters = create_chapters(subjects)
    
    # 8. Create Lessons
    print("\n📝 Creating lessons...")
    lessons = create_lessons(subjects, chapters)
    
    # 9. Create Questions
    print("\n❓ Creating questions...")
    questions = create_questions(subjects, lessons, years)
    
    # 10. Create Coupons
    print("\n🎟️ Creating coupons...")
    create_coupons()
    
    # 11. Create User-specific data
    print("\n👨‍🎓 Creating user-specific data...")
    create_user_data(admin, lessons, questions)
    
    print("\n✅ Database seeding completed successfully!")
    print_summary(admin)


def create_plans():
    """Create subscription plans"""
    plans = {}
    
    plans['basic'] = Plan.objects.get_or_create(
        code='basic',
        defaults={
            'name': 'Basic Plan',
            'price_egp': Decimal('199.00'),
            'duration_days': 365,
            'is_active': True
        }
    )[0]
    
    plans['premium'] = Plan.objects.get_or_create(
        code='premium',
        defaults={
            'name': 'Premium Plan',
            'price_egp': Decimal('399.00'),
            'duration_days': 365,
            'is_active': True
        }
    )[0]
    
    plans['advanced'] = Plan.objects.get_or_create(
        code='advanced',
        defaults={
            'name': 'Advanced Plan',
            'price_egp': Decimal('599.00'),
            'duration_days': 365,
            'is_active': True
        }
    )[0]
    
    print(f"   ✓ Created {len(plans)} plans")
    return plans


def update_admin_user(premium_plan):
    """Update admin user with premium subscription"""
    try:
        # Use environment variable TEST_ADMIN_USERNME and default to testAdmin
        test_admin_username = os.environ.get('TEST_ADMIN_USERNAME', 'username')
        admin = User.objects.get(username=test_admin_username)
        admin.study_year = 'y3'  # Year 3
        admin.plan = 'premium'
        admin.is_active_subscription = True
        admin.activated_at = timezone.now()
        admin.expires_at = timezone.now() + timedelta(days=365)
        admin.save()
        
        # Create streak
        UserStreak.objects.get_or_create(
            user=admin,
            defaults={'current_streak': 5, 'last_active_date': date.today()}
        )
        
        print(f"   ✓ Updated user 'username' with Premium plan (Year 3)")
        return admin
    except User.DoesNotExist:
        print("   ⚠️  User 'username' not found. Please create it first.")
        return None


def create_years():
    """Create academic years"""
    years = {}
    year_data = [
        ('y1', 'Year 1', 1),
        ('y2', 'Year 2', 2),
        ('y3', 'Year 3', 3),
        ('y4', 'Year 4', 4),
        ('y5', 'Year 5', 5),
    ]
    
    for code, name, order in year_data:
        years[code] = Year.objects.get_or_create(
            code=code,
            defaults={'name': name, 'order': order}
        )[0]
    
    print(f"   ✓ Created {len(years)} years")
    return years


def create_semesters(years):
    """Create semesters for each year"""
    semesters = []
    
    for year_code, year in years.items():
        for sem_num in [1, 2]:
            semester = Semester.objects.get_or_create(
                year=year,
                name=f"Semester {sem_num}",
                defaults={'order': sem_num}
            )[0]
            semesters.append(semester)
    
    print(f"   ✓ Created {len(semesters)} semesters")
    return semesters


def create_modules(semesters):
    """Create modules for Year 3 semesters"""
    modules = []
    
    # Focus on Year 3 for the admin user
    y3_semesters = [s for s in semesters if s.year.code == 'y3']
    
    module_names = [
        'Cardiovascular System',
        'Respiratory System',
        'Gastrointestinal System',
        'Renal System',
        'Endocrine System',
        'Nervous System',
    ]
    
    for idx, semester in enumerate(y3_semesters):
        # 3 modules per semester
        for i in range(3):
            module_idx = (idx * 3) + i
            if module_idx < len(module_names):
                module = Module.objects.get_or_create(
                    semester=semester,
                    name=module_names[module_idx],
                    defaults={'order': i + 1, 'is_ready': True}
                )[0]
                modules.append(module)
    
    print(f"   ✓ Created {len(modules)} modules (Year 3)")
    return modules


def create_subjects(modules):
    """Create subjects for modules"""
    subjects = []
    
    subject_names = [
        'Anatomy',
        'Physiology',
        'Pathology',
        'Pharmacology',
        'Clinical Medicine',
    ]
    
    for module in modules:
        for idx, name in enumerate(subject_names):
            subject = Subject.objects.get_or_create(
                module=module,
                name=name,
                defaults={'order': idx + 1}
            )[0]
            subjects.append(subject)
    
    print(f"   ✓ Created {len(subjects)} subjects")
    return subjects


def create_chapters(subjects):
    """Create chapters for subjects"""
    chapters = []
    
    chapter_templates = [
        'Introduction and Overview',
        'Basic Concepts',
        'Clinical Applications',
        'Advanced Topics',
    ]
    
    # Create chapters for first 10 subjects
    for subject in subjects[:10]:
        for idx, template in enumerate(chapter_templates):
            chapter = Chapter.objects.get_or_create(
                subject=subject,
                order=idx + 1,
                defaults={'title': f"{template} - {subject.name}"}
            )[0]
            chapters.append(chapter)
    
    print(f"   ✓ Created {len(chapters)} chapters")
    return chapters


def create_lessons(subjects, chapters):
    """Create lessons for subjects"""
    lessons = []
    
    # Create lessons for first 10 subjects
    for subject in subjects[:10]:
        subject_chapters = [c for c in chapters if c.subject == subject]
        
        # 3 lessons per subject
        for i in range(3):
            chapter = subject_chapters[i % len(subject_chapters)] if subject_chapters else None
            
            lesson = Lesson.objects.get_or_create(
                subject=subject,
                title=f"Lesson {i+1}: {subject.name}",
                defaults={
                    'chapter': chapter,
                    'content': f"""
                    <h2>Welcome to {subject.name} - Lesson {i+1}</h2>
                    <p>This lesson covers important concepts in {subject.name}.</p>
                    <h3>Learning Objectives:</h3>
                    <ul>
                        <li>Understand the basic principles</li>
                        <li>Apply knowledge to clinical scenarios</li>
                        <li>Master key concepts for exams</li>
                    </ul>
                    <p><strong>Study tip:</strong> Review this material regularly and practice with questions.</p>
                    """,
                    'order': i + 1,
                    'part_type': 'theoretical' if i % 2 == 0 else 'practical'
                }
            )[0]
            lessons.append(lesson)
    
    print(f"   ✓ Created {len(lessons)} lessons")
    return lessons


def create_questions(subjects, lessons, years):
    """Create questions for subjects and lessons"""
    questions = []
    
    # MCQ Questions for lessons
    for lesson in lessons[:15]:
        for i in range(3):
            question = Question.objects.get_or_create(
                lesson=lesson,
                text=f"What is the main concept covered in {lesson.title}? (Question {i+1})",
                defaults={
                    'subject': lesson.subject,
                    'question_type': 'mcq',
                    'source_type': 'qbank',
                    'exam_kind': 'none',
                    'part_type': lesson.part_type,
                    'explanation': f"This question tests your understanding of {lesson.subject.name}."
                }
            )[0]
            
            if question.id:  # New question
                # Create options
                QuestionOption.objects.create(
                    question=question,
                    text=f"Correct answer about {lesson.subject.name}",
                    is_correct=True
                )
                QuestionOption.objects.create(
                    question=question,
                    text="Incorrect option A",
                    is_correct=False
                )
                QuestionOption.objects.create(
                    question=question,
                    text="Incorrect option B",
                    is_correct=False
                )
                QuestionOption.objects.create(
                    question=question,
                    text="Incorrect option C",
                    is_correct=False
                )
            
            questions.append(question)
    
    # Exam Review Questions
    y3 = years.get('y3')
    if y3:
        for subject in subjects[:5]:
            for i in range(2):
                question = Question.objects.get_or_create(
                    subject=subject,
                    year=y3,
                    text=f"Exam review question for {subject.name} - Question {i+1}",
                    defaults={
                        'question_type': 'mcq',
                        'source_type': 'exam_review',
                        'exam_kind': 'midterm',
                        'exam_year': '2024',
                        'part_type': 'theoretical',
                        'explanation': f"Review material for {subject.name} exams."
                    }
                )[0]
                
                if question.id:
                    QuestionOption.objects.create(question=question, text="Answer A", is_correct=True)
                    QuestionOption.objects.create(question=question, text="Answer B", is_correct=False)
                    QuestionOption.objects.create(question=question, text="Answer C", is_correct=False)
                
                questions.append(question)
    
    print(f"   ✓ Created {len(questions)} questions")
    return questions


def create_coupons():
    """Create discount coupons"""
    coupons = [
        ('WELCOME20', 20, None, None, 100),
        ('STUDENT50', 50, timezone.now(), timezone.now() + timedelta(days=30), 50),
        ('PREMIUM15', 15, None, None, None),  # Unlimited
    ]
    
    for code, percent, valid_from, valid_to, max_uses in coupons:
        Coupon.objects.get_or_create(
            code=code,
            defaults={
                'percent': Decimal(str(percent)),
                'valid_from': valid_from,
                'valid_to': valid_to,
                'max_uses_total': max_uses,
                'is_active': True
            }
        )
    
    print(f"   ✓ Created {len(coupons)} coupons")


def create_user_data(admin, lessons, questions):
    """Create user-specific data for admin"""
    if not admin:
        return
    
    # Favorite Lessons
    favorite_count = 0
    for lesson in lessons[:5]:
        FavoriteLesson.objects.get_or_create(
            user=admin,
            lesson=lesson
        )
        favorite_count += 1
    print(f"   ✓ Created {favorite_count} favorite lessons")
    
    # Lesson Progress
    progress_count = 0
    for lesson in lessons[:8]:
        LessonProgress.objects.get_or_create(
            user=admin,
            lesson=lesson,
            defaults={'is_done': True}
        )
        progress_count += 1
    print(f"   ✓ Created {progress_count} lesson progress records")
    
    # Flashcards
    flashcard_count = 0
    for lesson in lessons[:5]:
        FlashCard.objects.get_or_create(
            lesson=lesson,
            owner_type='user',
            owner=admin,
            question=f"What are the key points in {lesson.title}?",
            defaults={
                'answer': f"Key concepts: anatomy, physiology, clinical applications.",
                'order': 1
            }
        )
        flashcard_count += 1
    print(f"   ✓ Created {flashcard_count} flashcards")
    
    # Planner Tasks
    today = date.today()
    tasks = [
        ('Review Cardiovascular Anatomy', today, False),
        ('Study Respiratory Physiology', today + timedelta(days=1), False),
        ('Complete Practice Questions', today + timedelta(days=2), False),
        ('Prepare for Midterm', today + timedelta(days=7), False),
        ('Review Flashcards', today - timedelta(days=1), True),  # Completed
    ]
    
    for title, due_date, is_done in tasks:
        PlannerTask.objects.get_or_create(
            user=admin,
            title=title,
            due_date=due_date,
            defaults={
                'notes': f"Important: {title}",
                'is_done': is_done
            }
        )
    print(f"   ✓ Created {len(tasks)} planner tasks")
    
    # Study Sessions
    session_count = 0
    for i in range(5):
        StudySession.objects.create(
            user=admin,
            started_at=timezone.now() - timedelta(days=i),
            minutes=25 * (i + 1),
            source='pomodoro'
        )
        session_count += 1
    print(f"   ✓ Created {session_count} study sessions")
    
    # Question Attempts
    attempt_count = 0
    for question in questions[:20]:
        QuestionAttempt.objects.get_or_create(
            user=admin,
            question=question,
            defaults={
                'is_correct': attempt_count % 3 != 0  # 2/3 correct ratio
            }
        )
        attempt_count += 1
    print(f"   ✓ Created {attempt_count} question attempts")


def print_summary(admin):
    """Print summary of seeded data"""
    print("\n" + "="*60)
    print("📊 SEEDING SUMMARY")
    print("="*60)
    
    print(f"\n📚 Content:")
    print(f"   • Years: {Year.objects.count()}")
    print(f"   • Semesters: {Semester.objects.count()}")
    print(f"   • Modules: {Module.objects.count()}")
    print(f"   • Subjects: {Subject.objects.count()}")
    print(f"   • Chapters: {Chapter.objects.count()}")
    print(f"   • Lessons: {Lesson.objects.count()}")
    print(f"   • Questions: {Question.objects.count()}")
    
    print(f"\n💳 Subscriptions:")
    print(f"   • Plans: {Plan.objects.count()}")
    print(f"   • Coupons: {Coupon.objects.count()}")
    
    if admin:
        print(f"\n👤 User 'username' Data:")
        print(f"   • Study Year: {admin.study_year}")
        print(f"   • Plan: {admin.plan} (Premium)")
        print(f"   • Subscription Active: {admin.is_active_subscription}")
        print(f"   • Expires: {admin.expires_at.strftime('%Y-%m-%d') if admin.expires_at else 'N/A'}")
        print(f"   • Streak: {admin.streak.current_streak} days" if hasattr(admin, 'streak') else "")
        print(f"   • Favorites: {FavoriteLesson.objects.filter(user=admin).count()}")
        print(f"   • Progress: {LessonProgress.objects.filter(user=admin).count()} lessons")
        print(f"   • Flashcards: {FlashCard.objects.filter(owner=admin).count()}")
        print(f"   • Tasks: {PlannerTask.objects.filter(user=admin).count()}")
        print(f"   • Questions Attempted: {QuestionAttempt.objects.filter(user=admin).count()}")
    
    print("\n" + "="*60)
    print("🎉 You can now test the app!")
    print("="*60)
    print("\n🔑 Login Credentials:")
    print("   Username: username")
    print("   Password: test")
    print("\n🌐 Access:")
    print("   • Web: http://localhost:8000/")
    print("   • Admin: http://localhost:8000/admin/")
    print("   • API: http://localhost:8000/api/")
    print("\n💡 Test Features:")
    print("   • Browse lessons and modules")
    print("   • Answer questions")
    print("   • Create flashcards")
    print("   • Track progress")
    print("   • View dashboard")
    print("="*60 + "\n")


if __name__ == "__main__":
    seed_all()
