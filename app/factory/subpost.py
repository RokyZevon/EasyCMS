# -*- coding=utf-8 -*-

from app import db
from ..models import Postlabel, Post
from ..catch import get_label_by_id, get_meta_by_id


def update_post_meta(metaid):
    meta = get_meta_by_id(metaid)
    if meta:
        meta.meta_num = len(Post.query.filter_by(post_meta=metaid).all())
        db.session.add(meta)
        db.session.commit()

# 文章设置文章标签 and 文章更新文章标签
def set_post_label(labelinfo):

    postid = labelinfo['id']
    labellist = labelinfo['list']

    dellabellist = Postlabel.query.filter_by(post_id=postid).all()

    for dellabel in dellabellist:
        label = get_label_by_id(dellabel.label_id)
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


# 删除文章标签信息
def del_post_labels(postid):

    postlabels = Postlabel.query.filter_by(post_id=postid)
    labels = postlabels.all()

    for postlabel in labels:
        label = get_label_by_id(postlabel.label_id)
        label.label_num -= 1

        if label.label_num == 0:
            db.session.delete(label)

    postlabels.delete()

    db.session.commit()


