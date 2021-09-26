from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect
# from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# from flask_mail import Mail
from flask import Flask
import logging






app = Flask(__name__)

db = SQLAlchemy(app)


fbcrypt = Bcrypt(app)