from flask import Flask
from app.routes.auth_routes import AuthRoutes
from app.models.database import Database

def create_app():
    app = Flask(__name__)

    Database()

    auth_routes = AuthRoutes()

    app.register_blueprint(auth_routes.bp)

    return app