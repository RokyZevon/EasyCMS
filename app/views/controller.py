# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import *

from app import app
from ..models import *
from ..catch import *
from ..factory import *

# 主页
@app.route('/')
def index():
    posts = getAllPages()
    postList = []

    for post in posts:
        postInfo = {}
        postInfo['title'] = post.post_title
        postInfo['datetime'] = post.post_date
        postInfo['auther'] = (getUserById(post.user_id)).user_nicename
        postInfo['content'] = post.post_content[0:200]

        postList.append(postInfo)
    return render_template('index.html', postList=postList)

# 文章页
@app.route('/p/<string:id>.html')
def post(id):
    return 'Post ' + id

# 独立页面
@app.route('/<string:slug>')
def page(slug):
    return 'Page ' + slug

# 标签页
@app.route('/label/<string:slug>')
def label(slug):
    return 'Label ' + slug

# 分类页
@app.route('/meta/<string:slug>')
def meta(slug):
    return 'Meta ' + slug

# 登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login():

    loginForm = LoginForm()

    if loginForm.validate_on_submit():

        # 获取用户
        user = getUserByEmail(loginForm.login.data)
        if user is None:
            user = getUserByLoginName(loginForm.login.data)

        if user is not None and User.verify_password(user, loginForm.password.data):
            login_user(user, loginForm.remberme.data)
            return redirect(request.args.get('next') or url_for('index'))

        print user
        flash(u'用户名或密码错误！')

    return render_template('login.html', form=loginForm)

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功！')
    return redirect(url_for('index'))


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    print "start"

    if registerForm.validate_on_submit():
        userInfo = {}
        userInfo['login'] = registerForm.login.data
        userInfo['email'] = registerForm.email.data
        userInfo['nicename'] = registerForm.nicename.data
        userInfo['pass'] = registerForm.password.data
        userInfo['rule'] = UserRule['READER']
        addUser(userInfo)
        flash("注册成功，请验证邮箱后登录！")
        return redirect(url_for('login'))

    return render_template('register.html', form=registerForm)

# 个人中心
@app.route('/user/<string:userlogin>')
def profile(userlogin):
    user = getUserByLoginName(userlogin)
    if user is None:
        abort(404)

    infoForm = EditUserInfoFrom()
    passForm = EditUserPassFrom()
    unableUserForm = UnableUserFrom()

    if current_user.is_authenticated:
        if current_user.isAdmin() or current_user == user:
            infoForm.nicename.data = user.user_nicename
            if user.user_url is None:
                infoForm.url.data = 'http://'
            else:
                infoForm.url.data = user.user_url

    avatar ='http://gravatar.duoshuo.com/avatar/' + hashlib.md5(user.user_email).hexdigest() + '?s=230'
    return render_template('profile.html', user=user, avatar=avatar,
                           infoForm=infoForm, passForm=passForm, unableUserForm=unableUserForm)

# 文章存档
@app.route('/archive')
def archive():
    return 'Archive'
