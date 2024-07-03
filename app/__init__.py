from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    app.static_folder = 'assets'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    return app, login_manager

app, login_manager= create_app()

