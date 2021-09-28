from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
import logging



app = Flask(__name__)


from instance.config import app

db = SQLAlchemy(app)

#Migracja db
# db_migration = Migrate()


#Logi
file_handler = RotatingFileHandler('instance/logs/flask-books-library-app.log',
                                   maxBytes=16384,
                                   backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [%(funcName)s in %(filename)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

#Logger
app.logger.info('Uruchamianie aplikacji Flask Books Library App... ')

#Logowanie użytkowników
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
login.login_message_category = 'info'

#Hashowanie hasła
fbcrypt = Bcrypt(app)

#CSRF
csrf = CSRFProtect(app)

#Mail
mail = Mail(app)



from models import User


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Import the blueprints
from mod_budget import budget_blueprint
from mod_auth import users_blueprint


# Register the blueprints
app.register_blueprint(budget_blueprint)
app.register_blueprint(users_blueprint, url_prefix='/users')




if __name__ == '__main__':
    app.run(debug=True)