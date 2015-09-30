# -*- coding=utf-8 -*-

from app.models import *
from app import db
from .subpost import setPostLabel,setPostMeta

# 添加用户
def addUser(userinfo):
    user = User()
    user.user_login = userinfo['login']
    user.user_email = userinfo['email']
    user.user_nicename = userinfo['nicename']
    user.user_pass = userinfo['pass']
    user.user_rule = UserRule['READER']

    db.session.add(user)

    # 获取ID

    return user

# 添加文章
def addPost(postInfo):
    post = Post()
    post.post_title = postInfo['title']
    post.post_content = postInfo['content']
    post.post_date = postInfo['date']
    post.post_password = postInfo['pass']
    post.post_status = postInfo['status']
    post.user_id = postInfo['userId']

    db.session.add(post)


    # 获取ID

    # 添加文章分类
    setPostMeta(dict(id=post.post_id, list=postInfo['metas']))

    # 添加文章标签
    setPostLabel(dict(id=post.post_id, list=postInfo['labels']))

    return post

# 添加页面
def addPage(pageInfo):
    page = Page()
    page.page_title = pageInfo['title']
    page.page_content = pageInfo['content']
    page.page_date = pageInfo['date']
    page.page_password = pageInfo['pass']
    page.page_status = pageInfo['status']
    page.user_id = pageInfo['userId']

    db.session.add(page)

    #获取ID

    return page


# 添加文章分类
def addMeta(metaInfo):
    meta = Meta()
    meta.meta_name = metaInfo['name']
    meta.meta_slug = metaInfo['slug']
    meta.meta_describe = metaInfo['describe']

    db.session.add(meta)

    #获取ID

    return meta

# 添加标签
def addLabel(labelInfo):
    label = Label()
    label.label_name = labelInfo['name']
    label.label_slug = labelInfo['slug']

    db.session.add(label)

    # 获取ID

    return label