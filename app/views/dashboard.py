# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import *

from app import app
from ..models import *
from ..catch import *
from ..factory import *


# 仪表盘
@app.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html')


# 仪表盘 所有文章
@app.route('/admin/posts', methods=['GET', 'POST'])
@login_required
def posts():

    delform = DelPostForm()

    if request.method == 'POST':
        if delform.validate_on_submit():
            if delform.delId.data == delform.delCreateId.data:
                del_post(int(delform.delId.data))

    page = request.args.get('page', 1, type=int)
    type = request.args.get('type', 0, type=int)
    meta = request.args.get('metaid', 0, type=int)
    label = request.args.get('labelid', 0, type=int)
    user = request.args.get('userid', 0, type=int)

    list = []

    if meta != 0:
        list = get_posts_by_meta_id(metaid=meta, page=page, type=type, userid=user)
    elif label != 0:
        list = get_posts_by_label_id(labelid=label, page=page, type=type, userid=user)
    else:
        list = get_all_posts(page=page, type=type, userid=user)

    return render_template('admin/posts.html', list=list['list'], pagination=list['pagination'], delForm=delform)


mon = {1: u'一月', 2: u'二月', 3: u'三月', 4: u'四月', 5: u'五月', 6: u'六月',
                       7: u'七月', 8: u'八月', 9: u'九月', 10: u'十月', 11: u'十一月', 12: u'十二月'}


# 仪表盘 新建文章 编辑文章
@app.route('/admin/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    editform = EditPostForm()

    if request.method == 'POST':

        if editform.validate_on_submit():
            postinfo = {}
            if editform.id.data:
                postinfo['id'] = editform.id.data
            else:
                postinfo['userId'] = current_user.user_id
            postinfo['title'] = editform.title.data
            postinfo['content'] = editform.content.data
            if editform.datetime.data:
                tmp = editform.datetime.data.split(' ')
                date = tmp[0].split('-')

                string = ''
                for num in mon:
                    if mon[num] == date[1]:
                        string = '%s-%s-%s %s' % (date[0], num, date[2], tmp[1])

                postinfo['date'] = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
            else:
                postinfo['date'] = datetime.now()

            if editform.password.data:
                postinfo['pass'] = editform.password.data

            postinfo['status'] = editform.status.data
            if postinfo['status'] == PostStatus['RELEASED'] or postinfo['status'] == PostStatus['OVERHEAD']:
                if not current_user.isEditor():
                    postinfo['status'] = PostStatus['UNAUDITED']

            if editform.save.data:
                if not editform.id.data:
                    postinfo['status'] = PostStatus['DRAFT']

            postinfo['meta'] = editform.metas.data
            postinfo['labels'] = editform.labels.data.split(',')

            post = add_post(postinfo)
            editform.id.data = post.post_id

    if request.method == 'GET':
        id = request.args.get('postid')
        if id:
            post = get_post_by_id(id)

            if not post:
                abort(404)

            editform.id.data = id
            editform.title.data = post.post_title
            editform.content.data = post.post_content
            editform.datetime.data = post.post_date.strftime("%Y-") +\
                            mon[int(post.post_date.strftime("%m"))] + post.post_date.strftime("-%d %H:%M:%S")
            editform.metas.data = post.post_meta
            editform.labels.data = '1,2,3'
            editform.password.data = post.post_password
            editform.status.data = post.post_status

    return render_template('admin/editpost.html', form=editform)


# 仪表盘 分类目录管理 添加目录 删除目录 修改目录
@app.route('/admin/metas', methods=['GET', 'POST'])
@login_required
def metaedit():

    addForm = AddMetaForm()
    delForm = DelMetaForm()

    if request.method == 'POST':

        if addForm.validate_on_submit():
            metaInfo = {}
            metaInfo['name'] = addForm.addName.data
            metaInfo['slug'] = addForm.addSlug.data
            metaInfo['describe'] = addForm.addDescribe.data
            add_meta(metaInfo)

        editForm = EditMetaForm()

        if editForm.validate_on_submit():
            metaInfo = {}
            metaInfo['id'] = editForm.editId.data
            metaInfo['name'] = editForm.editName.data
            metaInfo['slug'] = editForm.editSlug.data
            metaInfo['describe'] = editForm.editDescribe.data
            add_meta(metaInfo)

        if delForm.validate_on_submit():
            meta = get_meta_by_id(delForm.delId.data)
            print meta
            if meta.meta_name == delForm.delName.data:
                delMeta(meta.meta_id)

    if request.method == 'GET':

        if request.args.get('metaid'):
            metaid = int(request.args.get('metaid'))
            meta = get_meta_by_id(metaid)

            editForm = EditMetaForm()
            editForm.editId.data = meta.meta_id
            editForm.editName.data = meta.meta_name
            editForm.editSlug.data = meta.meta_slug
            editForm.editDescribe.data = meta.meta_describe
            return render_template('admin/editmeta.html', editForm=editForm)

    page = request.args.get('page', 1, type=int)
    pagination = get_all_metas(page=page)
    metas = pagination.items

    list = []
    for meta in metas:
        tmp = {}
        tmp['name'] = meta.meta_name
        tmp['slug'] = meta.meta_slug
        tmp['id'] = meta.meta_id
        tmp['num'] = meta.meta_num

        list.append(tmp)

    return render_template('admin/metas.html', list=list, pagination=pagination, addForm=addForm, delForm=delForm)


# 仪表盘 标签管理 修改标签 删除目录
@app.route('/admin/labels', methods=['GET', 'POST'])
@login_required
def labeledit():

    delForm = DelLabelForm()
    editForm = EditLabelForm()

    if request.method == 'POST':

        if editForm.validate_on_submit():
            labelInfo = {}
            labelInfo['id'] = editForm.editId.data
            labelInfo['name'] = editForm.editName.data
            labelInfo['slug'] = editForm.editSlug.data
            add_label(labelInfo)

        if delForm.validate_on_submit():
            label = get_label_by_id(delForm.delId.data)
            if label.label_name == delForm.delName.data:
                delLabel(label.label_id)

    page = request.args.get('page', 1, type=int)
    pagination = get_all_label(page=page)
    labels = pagination.items
    list = []
    for label in labels:
        tmp = {}
        tmp['name'] = label.label_name
        tmp['slug'] = label.label_slug
        tmp['id'] = label.label_id
        tmp['num'] = label.label_num

        list.append(tmp)

    labels = get_all_label(page=0)
    yun = []
    for label in labels:
        tmp = {}
        tmp['name'] = label.label_name
        tmp['id'] = label.label_id
        tmp['num'] = label.label_num

        yun.append(tmp)

    return render_template('admin/labels.html', yun=yun, list=list, pagination=pagination, editForm=editForm, delForm=delForm)


# 仪表盘 页面管理
@app.route('/admin/pages', methods=['GET', 'POST'])
@login_required
def pages():
    delform = DelPageForm()

    if request.method == 'POST':
        if delform.validate_on_submit():
            if delform.delId.data == delform.delCreateId.data:
                del_page(int(delform.delId.data))

    page = request.args.get('page', 1, type=int)
    type = request.args.get('type', 0, type=int)
    user = request.args.get('userid', 0, type=int)

    list = get_all_pages(page=page, type=type, userid=user)

    return render_template('admin/pages.html', list=list['list'], pagination=list['pagination'], delForm=delform)


# 仪表盘 新建页面 编辑页面
@app.route('/admin/editpages', methods=['GET', 'POST'])
@login_required
def editpage():

    editform = EditPageForm()

    if request.method == 'POST':

        if editform.validate_on_submit():
            pageinfo = {}
            if editform.id.data:
                pageinfo['id'] = editform.id.data
            else:
                pageinfo['userId'] = current_user.user_id
            pageinfo['title'] = editform.title.data

            if 'slug' in pageinfo:
                pageinfo['slug'] = editform.slug.data
            else:
                pageinfo['slug'] = editform.title.data
                
            pageinfo['content'] = editform.content.data

            if editform.datetime.data:
                tmp = editform.datetime.data.split(' ')
                date = tmp[0].split('-')

                string = ''
                for num in mon:
                    if mon[num] == date[1]:
                        string = '%s-%s-%s %s' % (date[0], num, date[2], tmp[1])

                pageinfo['date'] = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
            else:
                pageinfo['date'] = datetime.now()

            if editform.password.data:
                pageinfo['pass'] = editform.password.data

            pageinfo['status'] = editform.status.data
            if pageinfo['status'] == PostStatus['RELEASED'] or pageinfo['status'] == PostStatus['OVERHEAD']:
                if not current_user.isEditor():
                    pageinfo['status'] = PostStatus['UNAUDITED']

            if editform.save.data:
                if not editform.id.data:
                    pageinfo['status'] = PostStatus['DRAFT']

            page = add_page(pageinfo)
            editform.id.data = page.page_id

    if request.method == 'GET':
        id = request.args.get('pageid', type=int)
        if id:
            page = get_page_by_id(id)

            if not page:
                abort(404)

            editform.id.data = id
            editform.title.data = page.page_title
            editform.content.data = page.page_content
            editform.slug.data = page.page_slug
            editform.datetime.data = page.page_date.strftime("%Y-") +\
                            mon[int(page.page_date.strftime("%m"))] + page.page_date.strftime("-%d %H:%M:%S")
            editform.password.data = page.page_password
            editform.status.data = page.page_status

    return render_template('admin/editpage.html', form=editform)


# 仪表盘 用户管理
@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def useredit():

    addForm = AddUserForm()
    editForm = EditUserForm()
    delForm = DelUserForm()

    if request.method == 'POST':

        if addForm.validate_on_submit():
            userInfo = {}
            userInfo['login'] = addForm.addLogin.data
            userInfo['email'] = addForm.addEmail.data
            userInfo['nicename'] = addForm.addNicename.data
            userInfo['pass'] = addForm.addPassword.data
            userInfo['rule'] = int(addForm.addRule.data)
            add_user(userInfo)
            flash(u"注册成功，请验证邮箱后登录！")

        if editForm.validate_on_submit():
            userInfo = {}
            userInfo['id'] = editForm.editId.data
            userInfo['login'] = editForm.editLogin.data
            userInfo['nicename'] = editForm.editNicename.data
            userInfo['url'] = editForm.editUrl.data
            userInfo['pass'] = editForm.editPassword.data
            userInfo['rule'] = int(editForm.editRule.data)
            add_user(userInfo)
            flash(u"用户信息修改成功！")

        if delForm.validate_on_submit():
            user = get_user_by_id(delForm.delId.data)
            if user.user_login == delForm.delLogin.data:
                delUser(int(delForm.delId.data))
                flash(u"用户删除成功！")
            else:
                flash(u"删除失败！")

    page = request.args.get('page', 1, type=int)
    pagination = get_all_user(page=page)
    userList = pagination.items

    list = []
    rule = {0: u'用户被禁用', 1: u'订阅者', 2: u'作 者', 3: u'编 辑', 4: u'管理员'}
    label = {0: 'label-default', 1: 'label-info', 2: 'label-primary', 3: 'label-success', 4: 'label-warning'}
    for user in userList:
        tmp = {}
        tmp['id'] = user.user_id
        tmp['login'] = user.user_login
        tmp['nicename'] = user.user_nicename
        tmp['email'] = user.user_email
        tmp['url'] = user.user_url
        tmp['rule'] = rule[user.user_rule]
        tmp['ruleId'] = user.user_rule
        tmp['label'] = label[user.user_rule]

        list.append(tmp)

    return render_template('admin/users.html', list=list, pagination=pagination, addForm=addForm, editForm=editForm, delForm=delForm)
