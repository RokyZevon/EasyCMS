# -*- coding=utf-8 -*-

from app import db
from ..models import Postmeta, Postlabel
from ..catch import getLabelById, getMetaById

# 文章设置文章分组 and 文章更新文章分类
def setPostMeta(metaInfo):

    postId = metaInfo['id']
    metaid = metaInfo['list']

    delmeta = Postmeta.query.filter_by(post_id=postId).first()
    if delmeta:
        umeta = getMetaById(delmeta.meta_id)
        umeta.meta_num -= 1
        db.session.add(umeta)

    db.session.query(Postmeta).filter(Postmeta.post_id == postId).delete()

    postMeta = Postmeta()
    postMeta.meta_id = metaid
    postMeta.post_id = postId

    umeta = getMetaById(metaid)
    umeta.meta_num += 1

    db.session.add(umeta)
    db.session.add(postMeta)
    db.session.commit()


# 文章设置文章标签 and 文章更新文章标签
def setPostLabel(labelinfo):

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

