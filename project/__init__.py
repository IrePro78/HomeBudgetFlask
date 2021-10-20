from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import logging


# Baza danych
from config import Config

db = SQLAlchemy()

# Migracja db
db_migration = Migrate()

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

    app.config.from_object('config.DevelopmentConfig')

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
    file_handler = RotatingFileHandler('instance/logs/home-budget-flask-app.log',
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
    app.logger.info('Uruchamianie aplikacji Home Budget Flask App... ')


def initialize_extensions(app):
    # Inicjalizacja bazy danych
    db.init_app(app)

    # Migracja bazy danych
    db_migration.init_app(app, db)

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

#
# def register_error_pages(app):
#     @app.errorhandler(404)
#     def page_not_found(e):
#         return render_template('404.html'), 404
#
#     @app.errorhandler(405)
#     def method_not_allowed(e):
#         return render_template('405.html'), 405
#
#     @app.errorhandler(403)
#     def page_forbidden(e):
#         return render_template('403.html'), 403
