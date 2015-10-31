# -*- coding=utf-8 -*-

from app.models import User, Post, Page, Meta, Label
from ..catch import get_post_by_id, get_user_by_id, getLabelByName, get_meta_by_id, get_label_by_id, get_page_by_id
from app import db
from .subpost import set_post_label, update_post_meta
import hashlib

# 添加用户 and 用户信息修改
def add_user(userinfo):

    user = User()
    getid = False

    # 获取ID
    if 'id' in userinfo:
        # 获取到ID说明是老用户修改信息流程
        user = get_user_by_id(userinfo['id'])
        getid = True
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

    # 密码
    if len(userinfo['pass']) > 0:
        user.updatePassword(userinfo['pass'])

    if 'url' in userinfo:
        user.user_url = userinfo['url']

    # 修改用户权限
    if 'rule' in userinfo:
        user.user_rule = userinfo['rule']

    # 数据持久化
    db.session.add(user)

    if getid is True:
        db.session.flush()

    db.session.commit()

    return user

# 添加文章 and 修改文章
def add_post(postinfo):

    post = Post()
    getid = False

    # 获取文章ID
    if 'id' in postinfo:
        post = get_post_by_id(postinfo['id'])
        getid = True

    if len(postinfo['title']) > 30:
        postinfo['title'] = postinfo['title'][0:30]
    post.post_title = postinfo['title']

    if len(postinfo['content']) > 5000:
        postinfo['content'] = postinfo['content'][0:5000]
    post.post_content = postinfo['content']

    post.post_date = postinfo['date']

    if 'pass' in postinfo:
        post.post_password = hashlib.md5(postinfo['pass']).hexdigest()

    post.post_status = postinfo['status']

    if 'userId' in postinfo:
        post.user_id = postinfo['userId']

    oldmeta = post.post_meta
    post.post_meta = postinfo['meta']

    db.session.add(post)
    update_post_meta(oldmeta)
    update_post_meta(post.post_meta)

    if getid is True:
        db.session.flush()

    db.session.commit()

    # 添加文章标签
    labellist = []

    for labelname in postinfo['labels']:
        if labelname:
            label = getLabelByName(labelname)
            if not label:
                label = add_label(dict(name=labelname, slug=labelname))
            labellist.append(label)

    set_post_label(dict(id=post.post_id, list=labellist))

    return post


# 添加页面 and 修改页面
def add_page(pageinfo):
    page = Page()
    getid = False

    # 获取页面ID
    if 'id' in pageinfo:
        page = get_page_by_id(pageinfo['id'])
        getid = True

    if len(pageinfo['title']) > 30:
        pageinfo['title'] = pageinfo['title'][0:30]
    page.page_title = pageinfo['title']

    # 默认短地址为标题
    if 'slug' in pageinfo:
        page.page_slug = pageinfo['slug']
    else:
        page.page_slug = page.page_title

    if len(pageinfo['content']) > 5000:
        pageinfo['content'] = pageinfo['content'][0:5000]
    page.page_content = pageinfo['content']

    page.page_date = pageinfo['date']

    if 'pass' in pageinfo:
        page.page_password = hashlib.md5(pageinfo['pass']).hexdigest()

    page.page_status = pageinfo['status']

    if 'userId' in pageinfo:
        page.user_id = pageinfo['userId']

    db.session.add(page)

    if getid is True:
        db.session.flush()

    db.session.commit()

    return page


# 添加文章分类 and 修改文章分类信息
def add_meta(metaInfo):
    meta = Meta()
    getid = False

    if 'id' in metaInfo:
        meta = get_meta_by_id(metaInfo['id'])
        getid = True
    else:
        meta.meta_num = 0

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

    if getid:
        db.session.flush()

    db.session.commit()

    return meta

# 添加标签 and 修改标签信息
def add_label(labelInfo):
    label = Label()

    getid = False

    if 'id' in labelInfo:
        label = get_label_by_id(labelInfo['id'])
        getid = True
    else:
        label.label_num = 0

    if len(labelInfo['name']) > 30:
        labelInfo['name'] = labelInfo['name'][0:30]
    label.label_name = labelInfo['name']

    if len(labelInfo['slug']) > 30:
        labelInfo['slug'] = labelInfo['slug'][0:30]
    label.label_slug = labelInfo['slug']

    db.session.add(label)

    if getid is True:
        db.session.flush()
    db.session.commit()

    return label