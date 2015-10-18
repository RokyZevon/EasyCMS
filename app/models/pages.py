# coding=utf-8
from app import db
from markdown import markdown
import bleach

class Page(db.Model):

    '''页面表'''

    __tablename__ = 'pages'
    page_id = db.Column(db.Integer, primary_key=True)
    page_title = db.Column(db.Text, nullable=False)
    page_slug = db.Column(db.Text, nullable=False, unique=True)
    page_content = db.Column(db.Text)
    page_content_html = db.Column(db.Text)
    page_status = db.Column(db.Integer)
    page_password = db.Column(db.String(64))
    page_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    @staticmethod
    def on_changed_page_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'p']
        target.page_content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tars=allowed_tags, strip=True
        ))

    def __repr__(self):
        return '<Page % r>' % self.page_id

db.event.listen(Page.page_content, 'set', Page.on_changed_page_content)
