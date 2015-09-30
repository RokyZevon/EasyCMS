# coding=utf-8
from app import db

class User(db.Model):

    '''用户表'''

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(64), unique=True, nullable=False)
    user_nicename = db.Column(db.String(64), unique=True)
    user_pass = db.Column(db.String(64), nullable=False)
    user_email = db.Column(db.String(64), unique=True, nullable=False)
    user_url = db.Column(db.String(64))
    user_rule = db.Column(db.Integer)

    posts = db.relationship('Post', backref='user')
    pages = db.relationship('Page', backref='user')

    def __repr__(self):
        return '<Users %r>' % self.user_id

    def __init__(self):
        pass

UserRule = {
    'ADMIN': 1,   # 管理员
    'EDITOR': 2,  # 编辑
    'AUTHER': 3,  # 作者
    'READER': 4   # 订阅者，读者
}