from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm



class RegisterForm(FlaskForm):
    username = StringField('Nazwa użytkownika', [DataRequired(), Length(min=5)])
    email = StringField('Email ', [DataRequired(), Email()])
    password = PasswordField('Hasło', [DataRequired(), Length(min=6)])
    # password_repeat = PasswordField('Powtórz Hasło', [validators.Length(min=6)])



class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika ', [DataRequired(), Length(min=5)])
    password = PasswordField('Hasło', [DataRequired(), Length(min=6)])
    remember_me = BooleanField('Pamiętaj Mnie')


class EmailForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email()])



class PasswordForm(FlaskForm):
    password = PasswordField('Nowe Hasło', [DataRequired(), Length(min=6)])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Obecne Hasło ', [DataRequired(), Length(min=6)])
    new_password = PasswordField('Nowe Hasło ', [DataRequired(), Length(min=6)])