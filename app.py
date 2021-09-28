from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
import logging

from project import create_app

app = create_app()




db = SQLAlchemy(app)


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
#
#
# # Import the blueprints
# from project.mod_budget import budget_blueprint
# from project.mod_auth import users_blueprint
#
#
# # Register the blueprints
# app.register_blueprint(budget_blueprint)
# app.register_blueprint(users_blueprint, url_prefix='/users')
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)