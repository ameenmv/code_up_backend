from flask import Flask, jsonify, request
from flask_login import LoginManager
from config import Config
from models import db, User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = None

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        response = jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        })
        response.status_code = 500
        
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'API شغّالة ✅'}), 200

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.courses import courses_bp
    from routes.quizzes import quizzes_bp
    from routes.certificates import certs_bp
    from routes.profile import profile_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(certs_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(analytics_bp)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database connection error: {e}")

    return app


app = create_app()

@app.route('/api/seed-database', methods=['GET'])
def seed_database():
    try:
        from seed_data import seed_logic
        with app.app_context():
            seed_logic()
        return jsonify({
            "message": "Database seeded successfully! You can now login as admin@platform.com with password admin123"
        }), 200
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
