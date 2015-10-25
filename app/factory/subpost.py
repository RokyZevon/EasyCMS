# -*- coding=utf-8 -*-

from app import db
from ..models import Postmeta, Postlabel
from ..catch import getLabelById


# 文章设置文章标签 and 文章更新文章标签
def set_post_label(labelinfo):

    postid = labelinfo['id']
    labellist = labelinfo['list']

    dellabellist = Postlabel.query.filter_by(post_id=postid).all()

    for dellabel in dellabellist:
        label = getLabelById(dellabel.label_id)
        label.label_num -= 1
        db.session.add(label)

    db.session.query(Postlabel).filter(Postlabel.post_id == postid).delete()

    for label in labellist:
        postlabel = Postlabel()
        postlabel.label_id = label.label_id
        postlabel.post_id = postid
        label.label_num += 1
        db.session.add(label)
        db.session.add(postlabel)

    db.session.commit()


# 删除文章分组信息
def delPostMetas(postId):

    Postmeta.query.filter_by(post_id=postId).delete()

# 删除文章标签信息
def delPostLabels(postId):

    Postlabel.query.filter_by(post_id=postId).delete()

