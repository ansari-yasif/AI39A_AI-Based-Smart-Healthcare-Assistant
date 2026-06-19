"""app/__init__.py — Application factory with global OAuth"""
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for, session  # added redirect, url_for, session
from config import get_config
from authlib.integrations.flask_client import OAuth
from datetime import timedelta

oauth = OAuth()

def create_app(env: str = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # Session lasts 7 days (browser close doesn't log out)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    oauth.init_app(app)

    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
        redirect_uri=app.config['GOOGLE_REDIRECT_URI']
    )

    _register_blueprints(app)
    _register_error_handlers(app)
    _register_context(app)
    _register_teardown(app)

    return app

def _register_blueprints(app):
    from app.routes.auth_routes       import auth_bp
    from app.routes.dashboard_routes  import dashboard_bp
    from app.routes.profile_routes    import profile_bp
    from app.routes.nutrition_routes  import nutrition_bp
    from app.routes.health_routes     import health_bp
    from app.routes.wellness_routes   import wellness_bp
    from app.routes.admin_routes      import admin_bp
    from app.routes.chat_routes       import chat_bp

    app.register_blueprint(auth_bp,       url_prefix='/auth')
    app.register_blueprint(dashboard_bp,  url_prefix='/dashboard')
    app.register_blueprint(profile_bp,    url_prefix='')
    app.register_blueprint(nutrition_bp,  url_prefix='/nutrition')
    app.register_blueprint(health_bp,     url_prefix='/health')
    app.register_blueprint(wellness_bp,   url_prefix='/wellness')
    app.register_blueprint(admin_bp,      url_prefix='/admin')
    app.register_blueprint(chat_bp)

    @app.route('/')
    def index():
        # Show homepage to everyone; pass logged_in flag for UI changes
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
                'role':      str(session.get('role') or 'user').lower().strip(),
                'avatar':    session.get('avatar',''),
                'logged_in': 'user_id' in session,
            }
        }

def _register_teardown(app):
    from app.models.database import close_db
    app.teardown_appcontext(close_db)