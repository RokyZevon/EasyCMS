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
    # posts = get_all_posts()
    # postlist = posts['list']
    postlist = []

    return render_template('index.html', postList=postlist)


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

    loginform = LoginForm()

    if loginform.validate_on_submit():

        # 获取用户
        user = getUserByEmail(loginform.login.data)
        if user is None:
            user = getUserByLoginName(loginform.login.data)

        if user is not None and User.verify_password(user, loginform.password.data):
            login_user(user, loginform.remberme.data)
            print request.args.get('next')
            return redirect(request.args.get('next') or url_for('index'))

        print user
        flash(u'用户名或密码错误！')

    return render_template('login.html', form=loginform)


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
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        userInfo = {}
        userInfo['login'] = registerform.login.data
        userInfo['email'] = registerform.email.data
        userInfo['nicename'] = registerform.nicename.data
        userInfo['pass'] = registerform.password.data
        userInfo['rule'] = UserRule['READER']
        add_user(userInfo)
        flash(u"注册成功，请验证邮箱后登录！")
        return redirect(url_for('login'))

    return render_template('register.html', form=registerform)


# 文章存档
@app.route('/archive')
def archive():
    return 'Archive'


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
            infoForm.editILogin.data = user.user_login
            infoForm.editINicename.data = user.user_nicename
            if user.user_url is None or user.user_url == '':
                infoForm.editIUrl.data = 'http://'
            else:
                infoForm.editIUrl.data = user.user_url
            passForm.editLogin.data = user.user_login
            unableUserForm.unableLogin.data = user.user_login

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

    if request.method == 'POST':
        if infoForm.validate_on_submit():
            userLogin = infoForm.editILogin.data
            if current_user.user_login == userLogin or current_user.isAdmin():
                user = getUserByLoginName(userLogin)
                user.user_nicename = infoForm.editINicename.data
                user.user_url = infoForm.editIUrl.data
                db.session.add(user)
                db.session.commit()
                flash(u'资料修改成功！')
            else:
                abort(403)

            return redirect(url_for('profile', userlogin=userLogin))

        if passForm.validate_on_submit():
            userLogin = passForm.editLogin.data
            if current_user.user_login == userLogin or current_user.isAdmin():
                user = getUserByLoginName(userLogin)

                user.updatePassword(passForm.editPpassword.data)
                db.session.add(user)
                db.session.commit()
                flash(u'密码修改成功，下次登录将使用新密码！')
            else:
                abort(403)
            return redirect(url_for('profile', userlogin=userLogin))

        if unableUserForm.validate_on_submit():
            userLogin = unableUserForm.unableLogin.data
            if current_user.user_login == userLogin or current_user.isAdmin():
                user = getUserByLoginName(userLogin)

                if user:
                    if user.user_login == unableUserForm.unableName.data:
                        user.user_rule = UserRule['DISABLE']
                        db.session.add(user)
                        db.session.commit()
                        flash(u'用户：' + userLogin + u' 已经被禁用，如需启用请联系管理员！')
                    else:
                        flash(u'用户登录名确认失败！')

            else:
                abort(403)
            return redirect(url_for('profile', userlogin=userLogin))

    userLogin = unableUserForm.unableLogin.data

    return redirect(url_for('profile', userlogin=userLogin))
