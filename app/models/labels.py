# coding=utf-8
from app import db

class Label(db.Model):

    '''标签表'''

    __tablename__ = 'labels'
    label_id = db.Column(db.Integer,primary_key=True)
    label_name = db.Column(db.String,nullable=False)

    postlabels = db.relationship('Postlabel',backref='labels')

    def __repr__(self):
        return '<Label %r>' % self.label_id

class Postlabel(db.Model):

    '''文章，标签对应表'''

    __tablename__ = 'psotlabels'
    label_id = db.Column(db.Integer,db.ForeignKey('labels.label_id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.post_id'))

    def __repr__(self):
        return '<Postlabel postId:%r == labelId:%r>' % (self.post_id,self.label_id)