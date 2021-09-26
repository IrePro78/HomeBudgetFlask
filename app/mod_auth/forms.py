from wtforms import Form, StringField, PasswordField, BooleanField, validators



class RegisterForm(Form):
    username = StringField('Username :', [validators.Length(min=5)])
    password = PasswordField('Password :', [validators.Length(min=6)])
    email = StringField('email', [validators.Email()])



class LoginForm(Form):
    username = StringField('Username :', [validators.Length(min=5)])
    password = PasswordField('Password :', [validators.Length(min=6)])
    remember_me = BooleanField('Remember Me')


class EmailForm(Form):
    email = StringField('email', [validators.Email()])



class PasswordForm(Form):
    password = PasswordField('New password :', [validators.Length(min=6)])


class ChangePasswordForm(Form):
    current_password = PasswordField('Current Password: ', [validators.Length(min=6)])
    new_password = PasswordField('New Password: ', [validators.Length(min=6)])