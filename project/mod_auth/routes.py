from flask import render_template, flash, redirect, url_for, request, abort, current_app, copy_current_request_context
from project.mod_auth.forms import RegisterForm, LoginForm, EmailForm, PasswordForm, ChangePasswordForm, EditForm
from flask_login import login_user, current_user, login_required, logout_user
from itsdangerous import URLSafeTimedSerializer, BadSignature
from sqlalchemy.exc import IntegrityError
from project.mod_auth import users_blueprint
from urllib.parse import urlparse
from flask_mail import Message
from datetime import datetime
from threading import Thread
from project import db, mail
from models import User





def generate_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    password_reset_url = url_for('users.process_password_reset_token',
                                 token=password_reset_serializer.dumps(user_email, salt='@4Dd4%3!%$#sdA*73$^4!'),
                                 _external=True)

    return Message(subject='Flask Books Library App - Żądanie zresetowania hasła!',
                   html=render_template('users/email_password_reset.html', password_reset_url=password_reset_url),
                   recipients=[user_email])



@users_blueprint.route('/password_reset_via_email', methods=['GET', 'POST'])
def password_reset_via_email():
    form = EmailForm()

    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Error! Nieprawidłowy adres email !', 'danger')
            return render_template('users/password_reset_via_email.html', form=form)

        if user.email_confirmed:
            @copy_current_request_context
            def send_email(email_message):
                with current_app.app_context():
                    mail.send(email_message)

            message = generate_password_reset_email(form.email.data)
            email_thread = Thread(target=send_email, args=[message])
            email_thread.start()

            flash('Sprawdź e-mail, wysłano link do resetowania hasła.', 'success')
        else:
            flash('Twój adres e-mail musi zostać potwierdzony przed próbą zresetowania hasła.', 'danger')
        return redirect(url_for('users.login'))

    return render_template('users/password_reset_via_email.html', form=form)



@users_blueprint.route('/password_reset_via_token/<token>', methods=['GET', 'POST'])
def process_password_reset_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='@4Dd4%3!%$#sdA*73$^4!', max_age=3600)
    except BadSignature as e:
        flash('Link do resetowania hasła jest nieprawidłowy lub wygasł', 'danger')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('Adres email jest nieprawidłowy!', 'error')
            return redirect(url_for('users.login'))
        user.updated_on = datetime.now()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Twoje hasło zostało zaktualizowane!', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/reset_password_with_token.html', form=form)



@users_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.is_password_correct(form.current_password.data):
            current_user.set_password(form.new_password.data)
            current_user.updated_on = datetime.now()
            db.session.add(current_user)
            db.session.commit()
            flash('Hasło zostało zmienione!', 'success')
            current_app.logger.info(f'Password updated for user: {current_user.username}')
            return redirect(url_for('users.user_profile'))
        else:
            flash('Błąd! Aktualne hasło jest nieprawidłowe!', 'danger')
            current_app.logger.info(f'Incorrect password change for user: {current_user.username}')
    return render_template('users/change_password.html', form=form)



@users_blueprint.route('/resend_email_confirmation', methods=['GET', 'POST'])
@login_required
def resend_email_confirmation():
    @copy_current_request_context
    def send_email(email_message):
        with current_app.app_context():
            mail.send(email_message)

    message = generate_confirmation_email(current_user.email)
    email_thread = Thread(target=send_email, args=[message])
    email_thread.start()

    flash('E-mail wysłany w celu potwierdzenia twojego adresu e-mail. Proszę sprawdzić email', 'success')
    current_app.logger.info(f'Email re-sent to confirm email address for user: {current_user.email}')
    return redirect(url_for('users.user_profile'))



@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Jesteś już zalogowany!', 'info')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.username}!')
        return redirect(url_for('budget.index'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and user.is_password_correct(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash(f'Dziękuję za zalogowanie {current_user.username}!', 'success')
                current_app.logger.info(f'Logged in user: {current_user.username}!')

                if not request.args.get('next'):
                    return redirect(url_for('users.user_profile'))

                next_url = request.args.get('next')
                if urlparse(next_url).scheme != '' or urlparse(next_url).netloc != '':
                    current_app.logger.info(f'Invalid next path in login request: {next_url}')
                    logout_user()
                    return abort(400)

                return redirect(next_url)
            flash('Bład! Nieprawidłowe dane logowania', 'danger')
            current_app.logger.error('Invalid user attempted to log in!')
    return render_template('users/login.html', form=form)



@users_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Do zobaczenia! ', 'info')
    return redirect(url_for('users.login'))



@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.password.data, form.email.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Dziękuję za rejestrację, {new_user.username} !Sprawdź swój adres e-mail,'
                      f' aby potwierdzić !', 'success')
                current_app.logger.info(f'Registered new user: {form.username.data}!')

                @copy_current_request_context
                def send_email(message):
                    with current_app.app_context():
                        mail.send(message)

                msg = generate_confirmation_email(form.email.data)
                email_thread = Thread(target=send_email, args=[msg])
                email_thread.start()

                return redirect(url_for('users.login'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Użytkownik ({form.username.data}) lub email ({form.email.data})'
                      f' już istnieje w bazie danych. ', 'warning')
        else:
            flash(' Wprowadzono błędne dane !', 'danger')

    return render_template('users/register.html', form=form)



@users_blueprint.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
   user = User.query.filter_by(id=current_user.id).first()
   db.session.delete(user)
   db.session.commit()

   flash(f'Twoje konto zostało skasowane.', 'success')
   return redirect(url_for('users.login'))



@users_blueprint.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('users/user_profile.html')




@users_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm(username=current_user.username, email=current_user.email)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass

    return render_template('users/edit_profile.html', form=form)






def generate_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('users.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='@4Dcert65573$^4!'),
                          _external=True)

    return Message(subject='Flask Books Library App - Potwierdź adres email',
                   html=render_template('users/email_confirmation.html', confirm_url=confirm_url),
                   recipients=[user_email])



@users_blueprint.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='@4Dcert65573$^4!', max_age=3600)
    except BadSignature as e:
        flash(f'Link potwierdzający jest nieprawidłowy lub wygasł.', 'danger')
        current_app.logger.info(f'Invalid or expired confirmation link received from IP address:'
                                f' {request.remote_addr}')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Konto już potwierdzone. Proszę się zalogować.', 'info')
        current_app.logger.info(f'Confirmation link received for a confirmed user: {user.username}')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Dziękuję za potwierdzenie adresu e-mail!', 'success')
        current_app.logger.info(f'Email address confirmed for: {user.email}')

    return redirect(url_for('budget.index'))