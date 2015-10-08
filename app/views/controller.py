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
            print request.args.get('next')
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
        flash(u"注册成功，请验证邮箱后登录！")
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
            infoForm.login.data = user.user_login
            infoForm.nicename.data = user.user_nicename
            if user.user_url is None:
                infoForm.url.data = 'http://'
            else:
                infoForm.url.data = user.user_url
            passForm.login.data = user.user_login
            unableUserForm.login.data = user.user_login

    avatar ='http://gravatar.duoshuo.com/avatar/' + hashlib.md5(user.user_email).hexdigest() + '?s=230'
    return render_template('profile.html', user=user, avatar=avatar,
                           infoForm=infoForm, passForm=passForm, unableUserForm=unableUserForm)

# 个人中心信息修改
@app.route('/proEdit', methods=['POST'])
@login_required
def proEdit():

    infoForm = EditUserInfoFrom()
    passForm = EditUserPassFrom()
    unableUserForm = UnableUserFrom()

    if infoForm.validate_on_submit():
        userLogin = infoForm.login.data
        if current_user.user_login == userLogin or current_user.isAdmin():
            user = getUserByLoginName(userLogin)
            user.user_nicename = infoForm.nicename.data
            user.user_url = infoForm.url.data
            db.session.add(user)
            db.session.commit()
            flash(u'资料修改成功！')
        else:
            abort(403)

        return redirect(url_for('profile', userlogin=userLogin))

    if passForm.validate_on_submit():
        userLogin = passForm.login.data
        if current_user.user_login == userLogin or current_user.isAdmin():
            user = getUserByLoginName(userLogin)

            user.updatePassword(passForm.password.data)
            db.session.add(user)
            db.session.commit()
            flash(u'密码修改成功，下次登录将使用新密码！')
        else:
            abort(403)
        return redirect(url_for('profile', userlogin=userLogin))

    if unableUserForm.validate_on_submit():
        userLogin = unableUserForm.login.data
        if current_user.user_login == userLogin or current_user.isAdmin():
            user = getUserByLoginName(userLogin)

            user.user_rule = UserRule['DISABLE']
            db.session.add(user)
            db.session.commit()
            flash(u'用户：' + userLogin + u' 已经被禁用，如需启用请联系管理员！')
        else:
            abort(403)
        return redirect(url_for('profile', userlogin=userLogin))

    abort(403)

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

    return render_template('admin/editpost.html', form=editForm)

# 文章存档
@app.route('/archive')
def archive():
    return 'Archive'
