from wtforms import Form, StringField, PasswordField, BooleanField, validators


class RegisterForm(Form):
    username = StringField('Nazwa użytkownika', [validators.Length(min=5)])
    email = StringField('Email ', [validators.Email()])
    password = PasswordField('Hasło', [validators.Length(min=6)])
    # password_repeat = PasswordField('Powtórz Hasło', [validators.Length(min=6)])



class LoginForm(Form):
    username = StringField('Nazwa użytkownika ', [validators.Length(min=5)])
    password = PasswordField('Hasło', [validators.Length(min=6)])
    remember_me = BooleanField('Pamiętaj Mnie')


class EmailForm(Form):
    email = StringField('Email', [validators.Email()])



class PasswordForm(Form):
    password = PasswordField('Nowe Hasło', [validators.Length(min=6)])


class ChangePasswordForm(Form):
    current_password = PasswordField('Obecne Hasło ', [validators.Length(min=6)])
    new_password = PasswordField('Nowe Hasło ', [validators.Length(min=6)])