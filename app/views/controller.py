# coding=utf-8
from app import app

# 主页
@app.route('/')
def index():
    return 'Hello World'

# 文章页
@app.route('/p/<int:id>.html')
def post():
    return 'Hello World'

# 独立页面
@app.route('/<string:slug>')
def page():
    return 'Hello World'

# 标签页
@app.route('/label/<string:slug>')
def label():
    return 'Hello World'

# 分类页
@app.route('/meta/<string:slug>')
def meta():
    return 'Hello World'

# 登陆页面
@app.route('/login')
def login():
    return 'Hello World'

# 文章存档
@app.route('/archive')
def archive():
    return 'Hello World'
