# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, ValidationError, HiddenField
from wtforms import DateTimeField, SelectField, TextAreaField

from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask.ext.pagedown.fields import PageDownField

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
    editILogin = HiddenField()
    editINicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    editIUrl = StringField(u'个人主页', validators=[Required(), Length(0, 64)])
    editISubmit = SubmitField(u'更新资料')

    def validate_editUrl(self, field):
        if field.data == 'http://':
            field.data = ''


# 个人中心修改个人密码表单
class EditUserPassFrom(Form):
    editLogin = HiddenField()
    editPpassword = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='两次输入的密码不一致！')])
    editPassword2 = PasswordField(u'确认密码', validators=[Required()])
    editSubmit = SubmitField(u'更新密码')


# 个人中心禁用用户表单
class UnableUserFrom(Form):
    unableLogin = HiddenField()
    unableName = StringField(u'确认登录名', validators=[Required(), Length(1, 64)])
    unableSubmit = SubmitField(u'确认禁用')


# 仪表盘 文章提交表单
class EditPostForm(Form):
    id = HiddenField()
    title = StringField(u'标题', validators=[Required(), Length(1, 64)])
    content = PageDownField(u'编辑内容', validators=[Required()])
    datetime = DateTimeField(u'发表时间', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required(), Length(0, 64)])
    status = SelectField(u'状态', coerce=int, default=PostStatus['RELEASED'])
    metas = SelectField(u'分类目录', coerce=int, default=1)
    labels = StringField(u'标签', validators=[Required(), Length(1, 64)])
    submit = SubmitField(u'发布')
    save = SubmitField(u'保存')


# 仪表盘 删除文章提交表单


# 仪表盘 页面提交表单
class EditPageForm(Form):
    id = HiddenField()
    title = StringField(u'标题', validators=[Required(), Length(1, 64)])
    slug = StringField(u'短地址', validators=[Required(), Length(1, 64)])
    content = PageDownField(u'编辑内容', validators=[Required()])
    datetime = DateTimeField(u'发表时间', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required(), Length(0, 64)])
    status = SelectField(u'状态', coerce=int, default=PostStatus['RELEASED'])
    submit = SubmitField(u'发布')
    save = SubmitField(u'保存')
# 仪表盘 删除页面提交表单


# 仪表盘 添加用户提交表单
class AddUserForm(Form):
    addLogin = StringField(u'登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    addEmail = StringField(u'常用邮箱', validators=[Required(), Length(1, 64), Email()])
    addNicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    addPassword = PasswordField(u'密码', validators=[Required()])
    addRule = SelectField(u'用户权限', coerce=int, choices=[(1, u"订阅者"), (2, u"作者"), (3, u"编辑"), (4, u"管理员"), (0, u"未激活用户")])
    addSubmit = SubmitField(u'添加用户')

    # def validate_addEmail(self, field):
    #     if getUserByEmail(field.data):
    #         raise ValidationError('邮箱已被使用！')
    #
    # def validate_addLogin(self, field):
    #     if getUserByLoginName(field.data):
    #         raise ValidationError('登录名已被使用！')


# 仪表盘 修改用户提交表单
class EditUserForm(Form):
    editId = HiddenField()
    editLogin = StringField(u'登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    editNicename = StringField(u'昵称', validators=[Required(), Length(1, 64)])
    editPassword = PasswordField(u'密码')
    editUrl = StringField(u'个人主页', validators=[Length(0, 64)])
    editRule = SelectField(u'用户权限', coerce=int, choices=[(1, u"订阅者"), (2, u"作者"), (3, u"编辑"), (4, u"管理员"), (0, u"禁用用户")],default=1)
    editSubmit = SubmitField(u'更新资料')

    def validate_editUrl(self, field):
        if field.data == 'http://':
            field.data = ''


# 仪表盘 删除用户提交表单
class DelUserForm(Form):
    delId = HiddenField()
    delLogin = StringField(u'确认登录名', validators=[Required(), Length(1, 64),
                                               Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, '登录名只允许是字母，数字，下划线')])
    delSubmit = SubmitField(u'确认删除')


# 仪表盘 添加分类目录提交表单
class AddMetaForm(Form):
    addName = StringField(u'分类名', validators=[Required(), Length(1, 64)])
    addSlug = StringField(u'别名', validators=[Required(), Length(1, 64)])
    addDescribe = TextAreaField(u'描述')
    addSubmit = SubmitField(u'添加分类')


# 仪表盘 修改分类目录提交表单
class EditMetaForm(Form):
    editId = HiddenField()
    editName = StringField(u'分类名', validators=[Required(), Length(1, 64)])
    editSlug = StringField(u'别名', validators=[Required(), Length(1, 64)])
    editDescribe = TextAreaField(u'描述')
    editSubmit = SubmitField(u'更新')


# 仪表盘 删除分类目录提交表单
class DelMetaForm(Form):
    delId = HiddenField()
    delName = StringField(u'分类目录名称', validators=[Required(), Length(1, 64)])
    delSubmit = SubmitField(u'确认删除')


# 仪表盘 添加分类目录提交表单
class EditLabelForm(Form):
    editId = HiddenField()
    editName = StringField(u'标签', validators=[Required(), Length(1, 64)])
    editSlug = StringField(u'别名', validators=[Required(), Length(1, 64)])
    editSubmit = SubmitField(u'更新')


# 仪表盘 删除分类目录提交表单
class DelLabelForm(Form):
    delId = HiddenField()
    delName = StringField(u'标签名称', validators=[Required(), Length(1, 64)])
    delSubmit = SubmitField(u'确认删除')

# 文章搜索表单


