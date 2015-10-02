# -*- coding=utf-8 -*-

from app import db
from ..models import Postmeta, Postlabel, Post

# 文章设置文章分组 and 文章更新文章分类
def setPostMeta(metaInfo):

    postId = metaInfo['id']
    metaList = metaInfo['list']

    oldList = Postmeta.query.filter_by(post_id=postId).all()

    # 清除原分组和新分组的交集
    for oldMeta in oldList:
        if oldMeta in metaList:
            metaList.pop(oldMeta)
            oldList.remove(oldMeta)

    # 从数据库删除旧数据
    for oldMeta in oldList:
        db.session.query(Postmeta).filter(Postmeta.post_id == postId).filter(Postmeta.meta_id == oldMeta).delete()

    # 添加新数据
    # 如果没有分组，分配到ID为1的默认分组
    if len(metaList) == 0:
        postMeta = Postmeta()
        postMeta.meta_id = 1
        postMeta.post_id = postId

    postMetaList = []

    for metaId in metaList:
        postMeta = Postmeta()
        postMeta.meta_id = metaId
        postMeta.post_id = postId
        postMetaList.append(postMeta)

    db.session.add_all(postMetaList)
    db.session.commit()
    db.session.close()

# 文章设置文章标签 and 文章更新文章标签
def setPostLabel(labelInfo):

    postId = labelInfo['id']
    labetList = labelInfo['list']

    oldList = Postlabel.query.filter_by(post_id=postId).all()

    # 清除原标签和新标签的交集
    for oldLabel in oldList:
        if oldLabel in labetList:
            labetList.pop(oldLabel)
            oldList.remove(oldLabel)

    # 从数据库删除旧数据
    for oldLabel in oldList:
        db.session.query(Postlabel).filter(Postlabel.post_id == postId).filter(Postlabel.meta_id == oldLabel).delete()

    postLabelList = []

    for labelId in labetList:
        postLabel = Postlabel()
        postLabel.post_id = postId
        postLabel.label_id = labelId
        postLabelList.append(postLabel)

    db.session.add_all(postLabelList)
    db.session.commit()
    db.session.close()

# 删除文章分组信息
def delPostMetas(postId):

    Postmeta.query.filter_by(post_id=postId).delete()

# 删除文章标签信息
def delPostLabels(postId):

    Postlabel.query.filter_by(post_id=postId).delete()

