# -*- coding=utf-8 -*-

from app.models import User, Post, Page, Meta, Label
from app import db
from .subpost import setPostLabel, setPostMeta
import hashlib

# 添加用户 and 用户信息修改
def addUser(userinfo):

    user = User()
    getId = False

    # 获取ID
    if 'id' in userinfo:
        # 获取到ID说明是老用户修改信息流程

        user = User.query.filter_by(user_id=userinfo['id']).first()
        getId = True
    else:
        # 获取不到ID说明为注册流程

        # 登陆名长度限制
        if len(userinfo['login']) > 30:
            userinfo['login'] = userinfo['login'][0:30]

        user.user_login = userinfo['login']

        user.user_email = userinfo['email']

    # 昵称长度限制
    if len(userinfo['nicename']) > 30:
        userinfo['nicename'] = userinfo['nicename'][0:30]
    user.user_nicename = userinfo['nicename']

    # 密码 用Email加盐MD5加密
    user.user_pass = hashlib.md5(userinfo['pass'] + user.user_email).hexdigest()

    # 修改用户权限
    if 'rule' in userinfo:
        user.user_rule = userinfo['rule']

    # 数据持久化
    db.session.add(user)

    if getId is False:
        db.session.flush()

    db.commit()
    db.session.close()


    return user

# 添加文章 and 修改文章
def addPost(postInfo):

    post = Post()
    getId = False

    # 获取文章ID
    if 'id' in postInfo:
        post = Post.query.filter_by(post_id=postInfo['id']).first()
        getId = True

    if len(postInfo['title']) > 30:
        postInfo['title'] = postInfo['title'][0:30]
    post.post_title = postInfo['title']

    if len(postInfo['content']) > 5000:
        postInfo['content'] = postInfo['content'][0:5000]
    post.post_content = postInfo['content']

    post.post_date = postInfo['date']

    if 'pass' in postInfo:
        post.post_password = hashlib.md5(postInfo['pass']).hexdigest()

    post.post_status = postInfo['status']
    post.user_id = postInfo['userId']

    db.session.add(post)

    if getId is False:
        db.session.flush()

    db.commit()
    db.session.close()

    # 添加文章分类
    setPostMeta(dict(id=post.post_id, list=postInfo['metas']))

    # 添加文章标签
    setPostLabel(dict(id=post.post_id, list=postInfo['labels']))

    return post

# 添加页面 and 修改页面
def addPage(pageInfo):
    page = Page()
    getId = False

    # 获取页面ID
    if 'id' in pageInfo:
        page = Page.query.filter_by(page_id = pageInfo['id']).first()
        getId = True

    if len(pageInfo['title']) > 30:
        pageInfo['title'] = pageInfo['title'][0,30]
    page.page_title = pageInfo['title']

    if len(pageInfo['content']) > 5000:
        pageInfo['content'] = pageInfo['content'][0:5000]
    page.page_content = pageInfo['content']

    page.page_date = pageInfo['date']

    if 'pass' in pageInfo:
        page.page_password = hashlib.md5(pageInfo['pass']).hexdigest()

    page.page_status = pageInfo['status']
    page.user_id = pageInfo['userId']

    db.session.add(page)

    if getId is False:
        db.session.flush()

    db.session.commit()
    db.session.close()

    return page


# 添加文章分类 and 修改文章页面
def addMeta(metaInfo):
    meta = Meta()

    if len(metaInfo['name']) > 30:
        metaInfo['name'] = metaInfo['name'][0:30]
    meta.meta_name = metaInfo['name']

    if len(metaInfo['slug']) > 30:
        metaInfo['slug'] = metaInfo['slug'][0:30]
    meta.meta_slug = metaInfo['slug']

    if len(metaInfo['describe']) > 200:
        metaInfo['describe'] = metaInfo['describe'][0:200]
    meta.meta_describe = metaInfo['describe']

    db.session.add(meta)
    db.session.flush()
    db.session.commit()
    db.session.close()

    return meta

# 添加标签 and 修改标签
def addLabel(labelInfo):
    label = Label()

    if len(labelInfo['name']) > 30:
        labelInfo['name'] = labelInfo['name'][0:30]
    label.label_name = labelInfo['name']

    if len(labelInfo['slug']) > 30:
        labelInfo['slug'] = labelInfo['slug'][0:30]
    label.label_slug = labelInfo['slug']

    db.session.add(label)
    db.session.flush()
    db.session.commit()
    db.session.close()

    return label