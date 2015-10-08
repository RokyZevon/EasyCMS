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

    def updatePassword(self, password):
        self.user_pass = hashlib.md5(password + self.user_email).hexdigest()

    def isAdmin(self):
        if self.user_rule == 4:
            return True
        return False

    def isEditor(self):
        if self.user_rule > 2:
            return True
        return False

    def isAuther(self):
        if self.user_rule > 1:
            return True
        return False

    def is_active(self):
        if self.user_rule >= 1:
            return True
        return False

    def __repr__(self):
        return '<Users %r>' % self.user_id

UserRule = {
    'ADMIN': 4,   # 管理员
    'EDITOR': 3,  # 编辑
    'AUTHER': 2,  # 作者
    'READER': 1,  # 订阅者，读者
    'DISABLE': 0  # 用户被禁用
}