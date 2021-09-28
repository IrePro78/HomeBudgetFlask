from app import app


app.secret_key = 'tajnyKod'
app.config['SESSION_TYPE'] = 'memcached'
app.config['DEBUG'] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:admin123@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CSRF_COOKIE_SECURE'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'flaskdjangopython@gmail.com'
app.config['MAIL_PASSWORD'] = '*********'
app.config['MAIL_DEFAULT_SENDER'] = 'admin@gmail.pl'