from os import getenv


FLASK_ENV = 'development'
DEBUG = True
TESTING = False
SECRET_KEY = getenv('SECRET_KEY')


SESSION_TYPE = 'memcached'
TEMPLATES_AUTO_RELOAD = True

SQLALCHEMY_DATABASE_URI = 'postgresql://app:admin123@db:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_COOKIE_SECURE = False

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'flaskdjangopython@gmail.com'
MAIL_PASSWORD = getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'admin@gmail.pl'


