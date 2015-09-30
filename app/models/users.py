# coding=utf-8
from app import db

class User(db.Model):

    '''用户表'''

    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    user_login = db.Column(db.String,unique=True)
    user_nicename = db.Column(db.String,unique=True)
    user_pass = db.Column(db.String)
    user_email = db.Column(db.String)
    user_url = db.Column(db.String)
    user_rule = db.Column(db.Integer)

    posts = db.relationship('Post',backref='users')
    pages = db.relationship('Page',backref='Users')

    def __repr__(self):
        return '<Users %r>' % self.user_id
