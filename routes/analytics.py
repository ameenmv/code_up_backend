from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import db, Course, Quiz, QuizAttempt, Enrollment, Certificate, LessonProgress
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated


@analytics_bp.route('/hardest-courses', methods=['GET'])
@login_required
@admin_required
def hardest_courses():
    """أكتر الكورسات اللي الطلاب بيفشلوا فيها من واقع quiz_attempts"""

    results = db.session.query(
        Course.id,
        Course.title_en,
        Course.title_ar,
        func.count(QuizAttempt.id).label('total_attempts'),
        func.sum(db.case((QuizAttempt.passed == False, 1), else_=0)).label('failed_attempts'),
        func.avg(QuizAttempt.score).label('avg_score')
    ).join(Quiz, Quiz.course_id == Course.id) \
     .join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id) \
     .group_by(Course.id) \
     .order_by(func.sum(db.case((QuizAttempt.passed == False, 1), else_=0)).desc()) \
     .all()

    data = []
    for r in results:
        total = r.total_attempts or 0
        failed = r.failed_attempts or 0
        fail_rate = round((failed / total) * 100, 1) if total > 0 else 0
        data.append({
            'course_id': r.id,
            'title': {'en': r.title_en, 'ar': r.title_ar},
            'total_attempts': total,
            'failed_attempts': failed,
            'fail_rate_percent': fail_rate,
            'avg_score': round(r.avg_score or 0, 1)
        })

    return jsonify(data), 200


@analytics_bp.route('/completion-time', methods=['GET'])
@login_required
@admin_required
def completion_time():
    """متوسط الوقت اللي الطالب بياخده عشان يخلص كورس"""

    results = db.session.query(
        Course.id,
        Course.title_en,
        Course.title_ar,
        func.count(Certificate.id).label('completions'),
        func.avg(
            func.extract('epoch', Certificate.issued_at - Enrollment.enrolled_at) / 86400.0
        ).label('avg_days')
    ).join(Enrollment, Enrollment.course_id == Course.id) \
     .join(Certificate, db.and_(
         Certificate.course_id == Course.id,
         Certificate.user_id == Enrollment.user_id
     )) \
     .group_by(Course.id) \
     .order_by(func.avg(
         func.extract('epoch', Certificate.issued_at - Enrollment.enrolled_at) / 86400.0
     ).asc()) \
     .all()

    data = []
    for r in results:
        avg_days = round(r.avg_days or 0, 1)
        data.append({
            'course_id': r.id,
            'title': {'en': r.title_en, 'ar': r.title_ar},
            'total_completions': r.completions,
            'avg_completion_days': avg_days,
            'avg_completion_label': {
                'en': f'{avg_days} days on average',
                'ar': f'متوسط {avg_days} يوم'
            }
        })

    return jsonify(data), 200


@analytics_bp.route('/overview', methods=['GET'])
@login_required
@admin_required
def overview():
    """نظرة عامة على المنصة"""

    total_students = db.session.query(func.count(Enrollment.user_id.distinct())).scalar()
    total_enrollments = Enrollment.query.count()
    total_completions = Certificate.query.count()
    total_quiz_attempts = QuizAttempt.query.count()
    passed_attempts = QuizAttempt.query.filter_by(passed=True).count()

    completion_rate = round((total_completions / total_enrollments) * 100, 1) if total_enrollments > 0 else 0
    quiz_pass_rate = round((passed_attempts / total_quiz_attempts) * 100, 1) if total_quiz_attempts > 0 else 0

    return jsonify({
        'total_students': total_students,
        'total_enrollments': total_enrollments,
        'total_completions': total_completions,
        'completion_rate_percent': completion_rate,
        'total_quiz_attempts': total_quiz_attempts,
        'quiz_pass_rate_percent': quiz_pass_rate
    }), 200


@analytics_bp.route('/search-history', methods=['GET'])
@login_required
@admin_required
def search_history():
    """أكتر الكلمات اللي الطلاب بيبحثوا عنها"""
    from models import SearchHistory

    # Top searched queries
    top_searches = db.session.query(
        SearchHistory.query,
        func.count(SearchHistory.id).label('count'),
        func.avg(SearchHistory.results_count).label('avg_results')
    ).group_by(SearchHistory.query) \
     .order_by(func.count(SearchHistory.id).desc()) \
     .limit(20) \
     .all()

    # Recent searches
    recent = SearchHistory.query.order_by(
        SearchHistory.searched_at.desc()
    ).limit(50).all()

    return jsonify({
        'top_searches': [{
            'query': r.query,
            'count': r.count,
            'avg_results': round(r.avg_results or 0, 1)
        } for r in top_searches],
        'recent_searches': [r.to_dict() for r in recent]
    }), 200
