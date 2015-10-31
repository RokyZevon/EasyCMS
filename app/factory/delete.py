# coding=utf-8

from app import db
from ..models import User, Post, Page, Postlabel, Label, Meta, PostStatus
from .subpost import update_post_meta, del_post_labels
from ..catch import get_posts_by_meta_id, get_posts_by_user_id, get_post_by_id, get_page_by_id


# 删除用户
def delUser(userid):

    # 对ID为1的用户进行保护，以保证至少有一个用户能登陆
    if userid is 1:
        return None

    postList = get_posts_by_user_id(userid)

    # 该用户发表的文章设置为默认编辑发表
    if postList:
        for post in postList:
            post.user_id = 1

        db.session.add_all(postList)

    # 删除用户信息
    User.query.filter_by(user_id=userid).delete()

    db.session.commit()

# 删除文章
def del_post(postid):

    post = get_post_by_id(postid)
    if post.post_status == PostStatus['DELETED']:
        # 更新相关标签信息
        del_post_labels(postid)

        # 删除文章
        Post.query.filter_by(post_id=postid).delete()

        # 更新相关分组信息
        oldmeta = post.post_meta
        update_post_meta(oldmeta)

    else:
        post.post_status = PostStatus['DELETED']

    db.session.commit()

# 删除页面
def del_page(pageid):

    page = get_page_by_id(pageid)
    if page.page_status == PostStatus['DELETED']:

        # 删除页面
        Page.query.filter_by(page_id=pageid).delete()
    else:
        page.page_status = PostStatus['DELETED']

    db.session.commit()

# 删除文章分类
def delMeta(metaId):

    postList = get_posts_by_meta_id(metaId)

    # 删除postList内的metaID的分组

    postMetaList = []

    # 直接删除会导致一些文章没有分组，则归属到默认分组

    db.session.add_all(postMetaList)

    # 删除文章分类信息
    Meta.query.filter_by(meta_id=metaId).delete()

    db.session.commit()

# 删除标签
def delLabel(labelId):

    Postlabel.query.filter_by(label_id=labelId).delete()
    Label.query.filter_by(label_id=labelId).delete()

    db.session.commit()
