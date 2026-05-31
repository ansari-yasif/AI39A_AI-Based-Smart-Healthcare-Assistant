"""app/__init__.py — Application factory"""
from flask import Flask, render_template
from config import get_config


def create_app(env: str = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_context(app)
    _register_teardown(app)
    return app


def _register_blueprints(app):
    from app.routes.auth_routes      import auth_bp
    # from app.routes.dashboard_routes import dashboard_bp
    # from app.routes.calorie_routes   import calorie_bp
    # from app.routes.meal_routes      import meal_bp
    # from app.routes.sleep_routes     import sleep_bp
    # from app.routes.mood_routes      import mood_bp
    # from app.routes.expense_routes   import expense_bp
    # from app.routes.ai_routes        import ai_bp
    # from app.routes.health_routes    import health_bp
    # from app.routes.admin_routes     import admin_bp
    # from app.routes.workout_routes   import workout_bp
    # from app.routes.weight_routes    import weight_bp
    # from app.routes.goal_routes      import goal_bp
    # from app.routes.report_routes    import report_bp
    # from app.routes.profile_routes   import profile_bp

    app.register_blueprint(auth_bp,      url_prefix='/auth')
    # app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    # app.register_blueprint(calorie_bp,   url_prefix='/calorie')
    # app.register_blueprint(meal_bp,      url_prefix='/meals')
    # app.register_blueprint(sleep_bp,     url_prefix='/sleep')
    # app.register_blueprint(mood_bp,      url_prefix='/mood')
    # app.register_blueprint(expense_bp,   url_prefix='/expense')
    # app.register_blueprint(ai_bp,        url_prefix='/ai')
    # app.register_blueprint(health_bp,    url_prefix='/health')
    # app.register_blueprint(admin_bp,     url_prefix='/admin')
    # app.register_blueprint(workout_bp,   url_prefix='/workout')
    # app.register_blueprint(weight_bp,    url_prefix='/weight')
    # app.register_blueprint(goal_bp,      url_prefix='/goals')
    # app.register_blueprint(report_bp,    url_prefix='/reports')
    # app.register_blueprint(profile_bp,   url_prefix='/profile')

    @app.route('/')
    def index():
        return render_template('index.html')


def _register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e): return render_template('errors/403.html'), 403
    @app.errorhandler(404)
    def not_found(e): return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def server_error(e): return render_template('errors/500.html'), 500


def _register_context(app):
    @app.context_processor
    def globals():
        from flask import session
        return {
            'app_name': app.config.get('APP_NAME', 'VitaPulse'),
            'current_user': {
                'id':        session.get('user_id'),
                'full_name': session.get('full_name',''),
                'email':     session.get('email',''),
                'role':      session.get('role','user'),
                'avatar':    session.get('avatar',''),
                'logged_in': 'user_id' in session,
            }
        }


def _register_teardown(app):
    from app.models.database import close_db
    app.teardown_appcontext(close_db)
