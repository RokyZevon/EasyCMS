# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from  wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..catch import getUserByLoginName, getUserByEmail

# 登陆表单
class LoginForm(Form):
    login = StringField(u'用户名或邮箱', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remberme = BooleanField(u'记住我', default=False)
    submit = SubmitField(u'登录')

# 注册（用户信息修改）表单
class RegisterForm(Form):
    login = StringField(u'登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    email = StringField(u'常用邮箱', validators=[Required(), Length(1, 64), Email()])
    nicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='两次输入的密码不一致！')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册新账户')

    def validate_email(self, field):
        if getUserByEmail(field.data):
            raise ValidationError('邮箱已被使用！')

    def validate_login(self, field):
        if getUserByLoginName(field.data):
            raise ValidationError('登录名已被使用！')

# 文章提交表单

# 文章搜索表单

# 页面提交表单

# 文章分类信息提交表单

# 标签信息提交表单
