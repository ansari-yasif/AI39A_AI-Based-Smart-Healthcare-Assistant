from flask import render_template

class AuthController:

    def home(self):
        return render_template("index.html")

    def login(self):
        return render_template("login.html")

    def register(self):
        return render_template("register.html")

    def logout(self):
        return "Logout Working"