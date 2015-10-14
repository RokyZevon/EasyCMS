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


# 仪表盘 新建文章 编辑文章
@app.route('/admin/users')
@login_required
def useredit():

    userList = getAllUsers()

    list = []
    rule = {0: u'用户被禁用', 1: u'订阅者', 2: u'作者', 3: u'编辑', 4: u'管理员'}
    label = {0: 'label-default', 1: 'label-info', 2: 'label-primary', 3: 'label-success', 4: 'label-warning'}
    for user in userList:
        tmp = {}
        tmp['id'] = user.user_id
        tmp['login'] = user.user_login
        tmp['nicename'] = user.user_nicename
        tmp['email'] = user.user_email
        tmp['rule'] = rule[user.user_rule]
        tmp['label'] = label[user.user_rule]

        list.append(tmp)

    return render_template('admin/users.html', list=list)
