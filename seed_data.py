from app import create_app
from models import db, User, Category, Course, Lesson, Quiz, Question, Choice

app = create_app()

def seed_logic():
    db.drop_all()
    db.create_all()

    if True:
        # ── Categories ──────────────────────────────────────────────
        categories = [
            Category(name_en='Web Development', name_ar='برمجة الويب', slug='web', icon='🌐',
                     description_en='Build websites and web apps', description_ar='تعلم بناء مواقع وتطبيقات الويب'),
            Category(name_en='Python', name_ar='Python', slug='python', icon='🐍',
                     description_en='The most popular programming language', description_ar='لغة البرمجة الأكثر شيوعاً'),
            Category(name_en='JavaScript', name_ar='JavaScript', slug='javascript', icon='⚡',
                     description_en='The language of the web', description_ar='لغة الويب الأساسية'),
            Category(name_en='Databases', name_ar='قواعد البيانات', slug='databases', icon='🗄️',
                     description_en='SQL and NoSQL', description_ar='SQL و NoSQL'),
            Category(name_en='Algorithms', name_ar='خوارزميات', slug='algorithms', icon='🧠',
                     description_en='Problem solving and algorithms', description_ar='حل المشكلات والخوارزميات'),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()

        web_cat   = Category.query.filter_by(slug='web').first()
        py_cat    = Category.query.filter_by(slug='python').first()
        js_cat    = Category.query.filter_by(slug='javascript').first()
        db_cat    = Category.query.filter_by(slug='databases').first()
        algo_cat  = Category.query.filter_by(slug='algorithms').first()

        # ── Admin ────────────────────────────────────────────────────
        admin = User(username='Admin', email='admin@platform.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        # ── Courses ──────────────────────────────────────────────────
        courses_data = [
            {
                'title_en': 'Python for Beginners - Zero to Hero',
                'title_ar': 'Python للمبتدئين - من الصفر للاحتراف',
                'description_en': 'A complete Python course from scratch. Learn variables, loops, functions, OOP and build real projects.',
                'description_ar': 'كورس شامل لتعلم Python من الصفر. هتتعلم المتغيرات، الحلقات، الدوال، OOP وكمان هتعمل مشاريع حقيقية.',
                'short_description_en': 'Learn Python step by step from zero',
                'short_description_ar': 'تعلم Python من الصفر خطوة بخطوة',
                'level': 'beginner', 'category': py_cat, 'duration_hours': 20,
                'lessons': [
                    {'title_en': 'Introduction: Why Python?', 'title_ar': 'مقدمة: ليه Python؟',
                     'description_en': 'Learn why Python is the best language for beginners', 'description_ar': 'نتعرف على Python وليه هي أفضل لغة للمبتدئين',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 15, 'order': 1, 'is_free_preview': True},
                    {'title_en': 'Installing Python & VS Code', 'title_ar': 'تثبيت Python وبيئة العمل',
                     'description_en': 'Install Python and VS Code and write your first program', 'description_ar': 'تثبيت Python وVS Code وأول برنامج',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 20, 'order': 2},
                    {'title_en': 'Variables & Data Types', 'title_ar': 'المتغيرات وأنواع البيانات',
                     'description_en': 'int, float, str, bool and arithmetic operations', 'description_ar': 'int, float, str, bool وعمليات الحساب',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 30, 'order': 3},
                    {'title_en': 'Conditions: if/else', 'title_ar': 'الجمل الشرطية if/else',
                     'description_en': 'Control the flow of your program', 'description_ar': 'التحكم في تدفق البرنامج',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 25, 'order': 4},
                    {'title_en': 'Loops: for & while', 'title_ar': 'الحلقات: for و while',
                     'description_en': 'Repeat code efficiently', 'description_ar': 'تكرار الكود بكفاءة',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 35, 'order': 5},
                    {'title_en': 'Functions', 'title_ar': 'الدوال Functions',
                     'description_en': 'Organize and reuse your code', 'description_ar': 'تنظيم الكود وإعادة الاستخدام',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 40, 'order': 6},
                    {'title_en': 'Lists & Dictionaries', 'title_ar': 'القوائم والقواميس',
                     'description_en': 'Lists, Dicts, Tuples', 'description_ar': 'Lists, Dicts, Tuples',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 45, 'order': 7},
                    {'title_en': 'Project: Simple Calculator', 'title_ar': 'مشروع: حاسبة بسيطة',
                     'description_en': 'Apply everything in a real project', 'description_ar': 'تطبيق كل اللي اتعلمناه في مشروع حقيقي',
                     'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw', 'duration_minutes': 60, 'order': 8},
                ],
                'quiz': {
                    'title_en': 'Python Basics Quiz', 'title_ar': 'اختبار أساسيات Python',
                    'passing_score': 70,
                    'questions': [
                        {
                            'text_en': 'What is the output of: print(type(3.14))?',
                            'text_ar': 'ما هو ناتج: print(type(3.14))?',
                            'explanation_en': '3.14 is a float not int',
                            'explanation_ar': 'الرقم 3.14 هو float وليس int',
                            'choices': [
                                ('<class int>', '<class int>', False),
                                ('<class float>', '<class float>', True),
                                ('<class str>', '<class str>', False),
                                ('<class number>', '<class number>', False),
                            ]
                        },
                        {
                            'text_en': 'Which of the following defines a function correctly in Python?',
                            'text_ar': 'أي من التالي يعرّف دالة في Python بشكل صحيح؟',
                            'explanation_en': 'In Python we use the keyword def to define functions',
                            'explanation_ar': 'في Python نستخدم الكلمة المحجوزة def لتعريف الدوال',
                            'choices': [
                                ('function myFunc():', 'function myFunc():', False),
                                ('def myFunc():', 'def myFunc():', True),
                                ('define myFunc():', 'define myFunc():', False),
                                ('func myFunc():', 'func myFunc():', False),
                            ]
                        },
                    ]
                }
            },
            {
                'title_en': 'HTML & CSS - Build Websites',
                'title_ar': 'HTML & CSS - بناء مواقع الويب',
                'description_en': 'Learn to build beautiful responsive websites from scratch using HTML for structure and CSS for design.',
                'description_ar': 'تعلم بناء مواقع ويب جميلة ومتجاوبة من الصفر. HTML لهيكل الصفحة وCSS للتصميم.',
                'short_description_en': 'Build your first website from scratch',
                'short_description_ar': 'ابني موقعك الأول من الصفر',
                'level': 'beginner', 'category': web_cat, 'duration_hours': 15,
                'lessons': [
                    {'title_en': 'Introduction to HTML', 'title_ar': 'مقدمة في HTML',
                     'description_en': 'The basic structure of a web page', 'description_ar': 'هيكل صفحة الويب الأساسي',
                     'video_url': 'https://youtu.be/qz0aGYrrlhU', 'duration_minutes': 20, 'order': 1, 'is_free_preview': True},
                    {'title_en': 'Basic HTML Elements & Tags', 'title_ar': 'العناصر والوسوم الأساسية',
                     'description_en': 'headings, paragraphs, links, images', 'description_ar': 'headings, paragraphs, links, images',
                     'video_url': 'https://youtu.be/qz0aGYrrlhU', 'duration_minutes': 30, 'order': 2},
                    {'title_en': 'Introduction to CSS', 'title_ar': 'مقدمة في CSS',
                     'description_en': 'Selectors, Properties, Values', 'description_ar': 'Selectors, Properties, Values',
                     'video_url': 'https://youtu.be/qz0aGYrrlhU', 'duration_minutes': 30, 'order': 3},
                    {'title_en': 'FlexBox', 'title_ar': 'FlexBox',
                     'description_en': 'Layout elements easily', 'description_ar': 'تنسيق العناصر بسهولة',
                     'video_url': 'https://youtu.be/qz0aGYrrlhU', 'duration_minutes': 40, 'order': 4},
                    {'title_en': 'Responsive Design', 'title_ar': 'التصميم المتجاوب',
                     'description_en': 'Media Queries and Mobile-First', 'description_ar': 'Media Queries و Mobile-First',
                     'video_url': 'https://youtu.be/qz0aGYrrlhU', 'duration_minutes': 35, 'order': 5},
                ],
                'quiz': None
            },
            {
                'title_en': 'JavaScript Fundamentals',
                'title_ar': 'JavaScript الأساسيات',
                'description_en': 'Learn JavaScript, the language of the web. Master DOM manipulation, Events, and Async Programming.',
                'description_ar': 'تعلم JavaScript لغة الويب. هتتعلم DOM manipulation وEvents والـ Async Programming.',
                'short_description_en': 'Make your website interactive with JavaScript',
                'short_description_ar': 'اجعل موقعك تفاعلياً مع JavaScript',
                'level': 'intermediate', 'category': js_cat, 'duration_hours': 25,
                'lessons': [
                    {'title_en': 'Introduction to JavaScript', 'title_ar': 'مقدمة في JavaScript',
                     'description_en': 'What is JS and how it works in the browser', 'description_ar': 'ما هو JS وكيف يعمل في المتصفح',
                     'video_url': 'https://youtu.be/W6NZfCO5SIk', 'duration_minutes': 20, 'order': 1, 'is_free_preview': True},
                    {'title_en': 'Variables: var, let, const', 'title_ar': 'المتغيرات: var, let, const',
                     'description_en': 'Difference between the three and their uses', 'description_ar': 'الفرق بين الثلاثة واستخداماتها',
                     'video_url': 'https://youtu.be/W6NZfCO5SIk', 'duration_minutes': 30, 'order': 2},
                    {'title_en': 'DOM Manipulation', 'title_ar': 'DOM Manipulation',
                     'description_en': 'Control HTML elements from JS', 'description_ar': 'التحكم في عناصر HTML من JS',
                     'video_url': 'https://youtu.be/W6NZfCO5SIk', 'duration_minutes': 45, 'order': 3},
                    {'title_en': 'Project: To-Do List', 'title_ar': 'مشروع: To-Do List',
                     'description_en': 'Complete app with Vanilla JS', 'description_ar': 'تطبيق كامل بـ Vanilla JS',
                     'video_url': 'https://youtu.be/W6NZfCO5SIk', 'duration_minutes': 80, 'order': 4},
                ],
                'quiz': None
            },
            {
                'title_en': 'SQL & Databases',
                'title_ar': 'SQL وقواعد البيانات',
                'description_en': 'Learn SQL from scratch and understand how to store and query data efficiently.',
                'description_ar': 'تعلم SQL من الصفر، وشوف ازاي تخزن وتستعلم عن البيانات بكفاءة.',
                'short_description_en': 'Master SQL and database management',
                'short_description_ar': 'أتقن SQL وإدارة قواعد البيانات',
                'level': 'beginner', 'category': db_cat, 'duration_hours': 12,
                'lessons': [
                    {'title_en': 'Introduction to Databases', 'title_ar': 'مقدمة في قواعد البيانات',
                     'description_en': 'What is a database and why we need it', 'description_ar': 'ما هي قاعدة البيانات ولماذا نحتاجها',
                     'video_url': 'https://youtu.be/HXV3zeQKqGY', 'duration_minutes': 20, 'order': 1, 'is_free_preview': True},
                    {'title_en': 'SELECT & WHERE', 'title_ar': 'SELECT و WHERE',
                     'description_en': 'Query and filter data', 'description_ar': 'استعلام البيانات وتصفيتها',
                     'video_url': 'https://youtu.be/HXV3zeQKqGY', 'duration_minutes': 35, 'order': 2},
                    {'title_en': 'JOIN & Relationships', 'title_ar': 'JOIN والعلاقات',
                     'description_en': 'INNER JOIN, LEFT JOIN, RIGHT JOIN', 'description_ar': 'INNER JOIN, LEFT JOIN, RIGHT JOIN',
                     'video_url': 'https://youtu.be/HXV3zeQKqGY', 'duration_minutes': 45, 'order': 3},
                ],
                'quiz': None
            },
        ]

        for data in courses_data:
            course = Course(
                title_en=data['title_en'], title_ar=data['title_ar'],
                description_en=data['description_en'], description_ar=data['description_ar'],
                short_description_en=data['short_description_en'], short_description_ar=data['short_description_ar'],
                level=data['level'], category_id=data['category'].id,
                instructor_id=admin.id, duration_hours=data['duration_hours'],
                is_published=True, is_free=True
            )
            db.session.add(course)
            db.session.flush()

            for l in data['lessons']:
                lesson = Lesson(
                    course_id=course.id,
                    title_en=l['title_en'], title_ar=l['title_ar'],
                    description_en=l.get('description_en', ''), description_ar=l.get('description_ar', ''),
                    video_url=l['video_url'], duration_minutes=l['duration_minutes'],
                    order=l['order'], is_free_preview=l.get('is_free_preview', False)
                )
                db.session.add(lesson)

            if data.get('quiz'):
                q = data['quiz']
                quiz = Quiz(
                    course_id=course.id,
                    title_en=q['title_en'], title_ar=q['title_ar'],
                    passing_score=q['passing_score'], is_published=True
                )
                db.session.add(quiz)
                db.session.flush()

                for idx, qst in enumerate(q['questions']):
                    question = Question(
                        quiz_id=quiz.id,
                        text_en=qst['text_en'], text_ar=qst['text_ar'],
                        explanation_en=qst.get('explanation_en', ''),
                        explanation_ar=qst.get('explanation_ar', ''),
                        order=idx + 1
                    )
                    db.session.add(question)
                    db.session.flush()

                    for c_en, c_ar, is_correct in qst['choices']:
                        choice = Choice(question_id=question.id, text_en=c_en, text_ar=c_ar, is_correct=is_correct)
                        db.session.add(choice)

        db.session.commit()
        print("✅ Seed data inserted!")
        print(f"📚 Courses: {Course.query.count()}")
        print(f"📖 Lessons: {Lesson.query.count()}")
        print(f"👤 Admin: admin@platform.com / admin123")

def seed():
    with app.app_context():
        seed_logic()

if __name__ == '__main__':
    seed()
