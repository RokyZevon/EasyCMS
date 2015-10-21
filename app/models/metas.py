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

    postmetas = db.relationship('Postmeta',backref='meta')

    def __repr__(self):
        return '<Meta %r>' % self.meta_id

class Postmeta(db.Model):

    '''文章分类明细表'''

    __tablename__ = 'postmetas'
    id = db.Column(db.Integer, primary_key=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('metas.meta_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return '<PostMeta postId:%r = metaId:%r>' % (self.post_id, self.meta_id)