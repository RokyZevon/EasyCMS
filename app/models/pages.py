# coding=utf-8
from app import db

class Page(db.Model):

    '''页面表'''

    __tablename__ = 'pages'
    page_id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.Text, nullable=False)
    page_content = db.Column(db.Text)
    page_status = db.Column(db.Integer)
    page_password = db.Column(db.String(64))
    page_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Page % r>' % self.page_id

PageStatus = {
    'UNAUDITED': 1,  # 未审核状态
    'DRAFT': 2,      # 草稿状态
    'RELEASED': 3,   # 已发布
    'PRIVATE': 4     # 私有状态
}