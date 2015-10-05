# coding=utf-8
import hashlib
from app import db
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):

    '''用户表'''

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(64), unique=True, nullable=False)
    user_nicename = db.Column(db.String(64), unique=True)
    user_pass = db.Column(db.String(128), nullable=False)
    user_email = db.Column(db.String(64), unique=True, nullable=False)
    user_url = db.Column(db.String(64))
    user_rule = db.Column(db.Integer)

    posts = db.relationship('Post', backref='user')
    pages = db.relationship('Page', backref='user')

    def get_id(self):
        return self.user_id

    def verify_password(self, password):
        password = hashlib.md5(password + self.user_email).hexdigest()
        if password == self.user_pass:
            return True
        return False

    def __repr__(self):
        return '<Users %r>' % self.user_id

UserRule = {
    'ADMIN': 1,   # 管理员
    'EDITOR': 2,  # 编辑
    'AUTHER': 3,  # 作者
    'READER': 4   # 订阅者，读者
}