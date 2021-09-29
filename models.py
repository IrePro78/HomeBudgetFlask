from sqlalchemy import func
from project import db, fbcrypt



class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.relationship('Category', backref='entry')


    def __init__(self, title, amount, category_id, user_id):
        self.title = title
        self.amount = amount
        self.category_id = category_id
        self.user_id = user_id


    def __str__(self):
        return self.title




class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


    def __init__(self, name: str):
        self.name = name


    def __str__(self):
        return self.name


#
# class Report(db.Model):
#     __tablename__ = "reports"
#


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime)
    email_confirmation_sent_on = db.Column(db.DateTime, server_default=func.now())
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_on = db.Column(db.DateTime)
    entries = db.relationship('Entry', cascade="all, delete, delete-orphan", backref='user', lazy='dynamic')



    def __init__(self, username: str, password_plaintext: str, email: str):
        self.email = email
        self.username = username
        self.password = self._generate_password_hash(password_plaintext)




    def is_password_correct(self, password_plaintext: str):
        return fbcrypt.check_password_hash(self.password, password_plaintext)


    def set_password(self, password_plaintext: str):
        self.password = self._generate_password_hash(
            password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return fbcrypt.generate_password_hash(
            password_plaintext).decode('utf-8')



    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
         return False

    def get_id(self):
        return str(self.id)


# db.create_all()












