from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm



class RegisterForm(FlaskForm):
    username = StringField('Nazwa użytkownika', [DataRequired(), Length(min=5, message=('Nazwa jest za krótka !'))])
    email = StringField('Email ', [DataRequired(), Email(message=('Nie prawidłowy adres email !'))])
    password = PasswordField('Hasło', [DataRequired(), Length(min=6, message=('Hasło jest za krótkie !'))])




class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika ', [DataRequired(), Length(min=5, message=('Nazwa jest za krótka !'))])
    password = PasswordField('Hasło', [DataRequired(), Length(min=6, message=('Hasło jest za krótkie !'))])
    remember_me = BooleanField('Pamiętaj Mnie')


class EditForm(FlaskForm):
    username = StringField('Nazwa użytkownika', [DataRequired(), Length(min=5, message=('Nazwa jest za krótka !'))])
    email = StringField('Email ', [DataRequired(), Email(message=('Nie prawidłowy adres email.'))])
    # password = PasswordField('Hasło', [DataRequired(), Length(min=6, message=('Hasło jest za krótkie.'))])



class EmailForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email(message=('Nie prawidłowy adres email !'))])



class PasswordForm(FlaskForm):
    password = PasswordField('Nowe Hasło', [DataRequired(), Length(min=6, message=('Hasło jest za krótkie !'))])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Obecne Hasło ', [DataRequired(), Length(min=6)])
    new_password = PasswordField('Nowe Hasło ', [DataRequired(), Length(min=6, message=('Hasło jest za krótkie !'))])