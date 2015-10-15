# -*- coding: utf-8 -*-
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
    return render_template('admin/base.html')


# 仪表盘 所有文章
@app.route('/admin/posts')
@login_required
def posts():
    return render_template('admin/posts.html')


# 仪表盘 新建文章 编辑文章
@app.route('/admin/editpost')
@login_required
def editpost():
    editForm = EditPostForm()
    editForm.metas.choices = [(1, u'默认目录')]
    editForm.status.choices = [(PostStatus['RELEASED'], u'已发布'), (PostStatus['DRAFT'], u'草稿'), (PostStatus['PRIVATE'], u'私有'),]

    return render_template('admin/editpost.html', form=editForm)


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
            addUser(userInfo)
            flash(u"注册成功，请验证邮箱后登录！")

        if editForm.validate_on_submit():
            userInfo = {}
            userInfo['id'] = editForm.editId.data
            userInfo['login'] = editForm.editLogin.data
            userInfo['nicename'] = editForm.editNicename.data
            userInfo['url'] = editForm.editUrl.data
            userInfo['pass'] = editForm.editPassword.data
            userInfo['rule'] = int(editForm.editRule.data)
            addUser(userInfo)
            flash(u"用户信息修改成功！")

        if delForm.validate_on_submit():
            user = getUserById(delForm.delId.data)
            if user.user_login == delForm.delLogin.data:
                delUser(int(delForm.delId.data))
                flash(u"用户删除成功！")
            else:
                flash(u"删除失败！")


    userList = getAllUsers()

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

    return render_template('admin/users.html', list=list, addForm=addForm, editForm=editForm, delForm=delForm)
