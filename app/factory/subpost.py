# -*- coding=utf-8 -*-

from app import db
from ..models import Postmeta, Postlabel, Post

# 文章设置文章分组 and 文章更新文章分类
def setPostMeta(metaInfo):

    postId = metaInfo['id']
    meta = metaInfo['list']

    db.session.query(Postmeta).filter(Postmeta.post_id == postId).delete()

    postMeta = Postmeta()
    postMeta.meta_id = meta
    postMeta.post_id = postId

    db.session.add(postMeta)
    db.session.commit()

# 文章设置文章标签 and 文章更新文章标签
def setPostLabel(labelInfo):

    postId = labelInfo['id']
    labelList = labelInfo['list']

    print postId
    print labelList

# 删除文章分组信息
def delPostMetas(postId):

    Postmeta.query.filter_by(post_id=postId).delete()

# 删除文章标签信息
def delPostLabels(postId):

    Postlabel.query.filter_by(post_id=postId).delete()

