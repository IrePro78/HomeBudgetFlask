from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask import Flask
import logging



def create_app():
    app = Flask(__name__)
# Configure Flask App
    app.config.from_pyfile('instance/flask.cfg')
    register_blueprints(app)
    configure_logging(app)
    return app


def register_blueprints(app):
    # Import the blueprints
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