# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, ValidationError, HiddenField, \
    DateTimeField
from wtforms.fields import SelectField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..catch import getUserByLoginName, getUserByEmail
from ..models import PostStatus


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


# 个人中心修改个人信息表单
class EditUserInfoFrom(Form):
    login = HiddenField()
    nicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    url = StringField(u'个人主页', validators=[Required(), Length(1, 64)])
    submit = SubmitField(u'更新资料')


# 个人中心修改个人密码表单
class EditUserPassFrom(Form):
    login = HiddenField()
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='两次输入的密码不一致！')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'更新密码')


# 个人中心禁用用户表单
class UnableUserFrom(Form):
    login = HiddenField()
    submit = SubmitField(u'确认禁用')


# 仪表盘 文章提交表单
class EditPostForm(Form):
    title = StringField(u'标题', validators=[Required(), Length(1, 64)])
    content = PageDownField(u'编辑内容', validators=[Required()])
    datetime = DateTimeField(u'发表时间', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required(), Length(0, 64)])
    status = SelectField(u'状态', default=[(PostStatus['RELEASED'], u"已发布")])
    metas = SelectField(u'分类目录', default=[("1", u"默认分类")])
    labels = StringField(u'标签', validators=[Required(), Length(1, 64)])
    submit = SubmitField(u'发布')
    save = SubmitField(u'保存')

# 仪表盘 删除文章提交表单

# 仪表盘 页面提交表单

# 仪表盘 删除页面提交表单


# 仪表盘 添加用户提交表单
class AddUserForm(Form):
    addLogin = StringField(u'登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    addEmail = StringField(u'常用邮箱', validators=[Required(), Length(1, 64), Email()])
    addNicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    addPassword = PasswordField(u'密码', validators=[Required()])
    addRule = SelectField(u'用户权限', default=[("1", u"订阅者")])
    addSubmit = SubmitField(u'添加新账户')

    def validate_email(self, field):
        if getUserByEmail(field.data):
            raise ValidationError('邮箱已被使用！')

    def validate_login(self, field):
        if getUserByLoginName(field.data):
            raise ValidationError('登录名已被使用！')


# 仪表盘 修改用户提交表单
class EditUserFrom(Form):
    editId = HiddenField()
    editLogin = StringField(u'登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    editNicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    editPassword = PasswordField(u'密码', validators=[Required()])
    editUrl = StringField(u'个人主页', validators=[Required(), Length(1, 64)])
    editRule = SelectField(u'用户权限', default=[("1", u"订阅者")])
    editSubmit = SubmitField(u'更新资料')

    def validate_login(self, field):
        if getUserByLoginName(field.data):
            raise ValidationError('登录名已被使用！')


# 仪表盘 删除用户提交表单
class DelUser(Form):
    delId = HiddenField()
    delSubmit = SubmitField(u'确认删除')


# 文章搜索表单

# 文章分类信息提交表单

# 标签信息提交表单
