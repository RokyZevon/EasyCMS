# coding=utf-8
from app import db

class Post(db.Model):

    '''文章表'''

    __tablename__ = 'posts'
    post_id = db.Column(db.Integer,primary_key=True)
    post_title = db.Column(db.Text,nullable=False)
    post_content = db.Column(db.Text)
    post_status = db.Column(db.Integer,nullable=False)
    post_password = db.Column(db.String)
    post_date = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))

    postmetas = db.relationship('Postmeta',backref='posts')
    postlabels = db.relationship('Postlabel',backref='posts')

    def __repr__(self):
        return '<Post % r>' % self.post_id
