from flask import Blueprint
from app.controllers.auth_controller import AuthController

class AuthRoutes:
    def __init__(self):
        self.bp = Blueprint("auth", __name__)

        self.controller = AuthController()

        self.bp.route("/", methods=["GET"])(self.controller.home)

        self.bp.route("/login", methods=["GET", "POST"])(self.controller.login)

        self.bp.route("/register", methods=["GET", "POST"])(self.controller.register)

        self.bp.route("/logout")(self.controller.logout)


auth_routes = AuthRoutes()