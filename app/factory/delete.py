# coding=utf-8

from app import db
from ..models import User, Post, Page, Postlabel, Postmeta, Label, Meta
from .subpost import delPostLabels, delPostMetas
from ..catch import getPostMetas, getPostsByUserId, getPostsByMetaId

# 删除用户
def delUser(userId):

    # 对ID为1的用户进行保护，以保证至少有一个用户能登陆
    if userId is 1:
        return None

    postList = getPostsByUserId(userId)

    # 该用户发表的文章设置为默认编辑发表
    if postList:
        for post in postList:
            post.user_id = 1

        db.session.add_all(postList)

    # 删除用户信息
    User.query.filter_by(user_id=userId).delete()

    db.session.commit()

# 删除文章
def delPost(postId):

    # 更新相关分组信息
    delPostMetas(postId)

    # 更新相关标签信息
    delPostLabels(postId)

    # 删除文章
    Post.query.filter_by(post_id=postId).delete()

    db.session.commit()
    db.session.close()

# 删除页面
def delPage(pageId):

    Page.query.filter_by(page_id=pageId).delete()

    db.session.commit()
    db.session.close()

# 删除文章分类
def delMeta(metaId):

    postList = getPostsByMetaId(metaId)

    # 删除postList内的metaID的分组
    Postmeta.query.filter_by(meta_id=metaId).delete()

    postMetaList = []

    # 直接删除会导致一些文章没有分组，则归属到默认分组
    for post in postList:
        if getPostMetas(post.post_id) is None:
            postMeta = Postmeta()
            postMeta.post_id = post.post_id
            postMeta.meta_id = 1
            postMetaList.append(postMeta)

    db.session.add_all(postMetaList)

    # 删除文章分类信息
    Meta.query.filter_by(meta_id=metaId).delete()

    db.session.commit()

# 删除标签
def delLabel(labelId):

    Postlabel.query.filter_by(label_id=labelId).delete()
    Label.query.filter_by(label_id=labelId).delete()

    db.session.commit()
