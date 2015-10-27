# coding=utf-8
from app import db

class Meta(db.Model):

    '''文章分类表'''

    __tablename__ = 'metas'
    meta_id = db.Column(db.Integer, primary_key=True)
    meta_name = db.Column(db.String(64), nullable=False, unique=True)
    meta_slug = db.Column(db.String(64), nullable=False, unique=True)
    meta_num = db.Column(db.Integer, nullable=False)
    meta_describe = db.Column(db.Text)

    posts = db.relationship('Post', backref='metas')

    def __repr__(self):
        return '<Meta %r>' % self.meta_id
