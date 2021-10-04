from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
import logging


# Baza danych
db = SQLAlchemy()


# Logowanie użytkowników
login = LoginManager()

# Hashowanie hasła
fbcrypt = Bcrypt()

# CSRF
csrf = CSRFProtect()

# Mail
mail = Mail()


def create_app():
    app = Flask(__name__)


    app.config.from_pyfile('/app/instance/flask.cfg')


    register_blueprints(app)
    configure_logging(app)
    initialize_extensions(app)

    return app


def register_blueprints(app):
    from project.mod_budget import budget_blueprint
    from project.mod_auth import users_blueprint

    app.register_blueprint(budget_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')


def configure_logging(app):
    # Logging Configuration
    file_handler = RotatingFileHandler('instance/logs/flask-books-library-app.log',
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [%(funcName)s in %(filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    # Logger
    app.logger.info('Uruchamianie aplikacji Flask Books Library App... ')


def initialize_extensions(app):
    # Inicjalizacja bazy danych
    db.init_app(app)

    # Logowanie użytkowników
    login.init_app(app)
    login.login_view = 'users.login'
    login.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
    login.login_message_category = 'info'

    from models import User


    # Create tables
    with app.app_context():
       db.create_all()

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Hashowanie hasła
    fbcrypt.init_app(app)

    # CSRF
    csrf.init_app(app)


    # Mail
    mail.init_app(app)

