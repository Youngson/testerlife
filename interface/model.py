from flask_login import  UserMixin
from . import db, bcrypt

db.create_all()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    userpassword = db.Column(db.String(100))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def is_correct_password(self, password):
        if User.query.filter_by(userpassword=password):
            return True

    @property
    def password(self):
        raise AttributeError('密码不是一个可读字段')


    @password.setter
    def password(self, _password):
        self.userpassword = bcrypt.generate_password_hash(_password)


    def verify_password(self, _password):
        return bcrypt.check_password_hash(self.userpassword, _password)
