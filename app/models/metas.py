# coding=utf-8
from app import db

class Meta(db.Model):

    '''文章分类表'''

    __tablename__ = 'metas'
    meta_id = db.Column(db.Integer,primary_key=True)
    meta_name = db.Column(db.String)
    meta_slug = db.Column(db.String,unique=True)
    meta_describe = db.Column(db.Text)

    postmetas = db.relationship('Postmeta',backref='metas')

    def __repr__(self):
        return '<Meta %r>' % self.meta_id

class PostMeta(db.Model):

    '''文章分类明细表'''

    __tablename__ = 'postmetas'
    meta_id = db.Column(db.Integer,db.ForeignKey('metas.meta_id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return '<PostMeta postId:%r = metaId:%r>' % (self.post_id,self.meta_id)