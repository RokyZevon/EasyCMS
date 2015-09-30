# -*- coding=utf-8 -*-

from app import db
from ..models import PostMeta,Postlabel


# 文章设置文章分组
def setPostMeta(metaInfo):

    postId = metaInfo['id']
    metaList = metaInfo['list']

    for metaId in metaList:
        postMeta = PostMeta()
        postMeta.meta_id = metaId
        postMeta.post_id = postId

        db.session.add(postMeta)

# 文章设置文章标签
def setPostLabel(labelInfo):

    postId = labelInfo['id']
    labetList = labelInfo['list']

    for labelId in labetList:
        postLabel = Postlabel()
        postLabel.post_id = postId
        postLabel.label_id = labelId

        db.session.add(postLabel)
