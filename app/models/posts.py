# coding=utf-8
from app import db
from markdown import markdown
import bleach

class Post(db.Model):

    '''文章表'''

    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.Text, nullable=False)
    post_content = db.Column(db.Text)
    post_content_html = db.Column(db.Text)
    post_status = db.Column(db.Integer, nullable=False)
    post_password = db.Column(db.String(64))
    post_date = db.Column(db.DateTime, nullable=False)
    post_meta = db.Column(db.Integer, db.ForeignKey('metas.meta_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    postlabels = db.relationship('Postlabel', backref='post')

    @staticmethod
    def on_changed_post_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'p']
        target.post_content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

    def __repr__(self):
        return '<Post % r>' % self.post_id

db.event.listen(Post.post_content, 'set', Post.on_changed_post_content)

PostStatus = {
    'DELETED': 0,  # 回收站状态
    'UNAUDITED': 1,  # 未审核状态
    'DRAFT': 2,      # 草稿状态
    'RELEASED': 3,   # 已发布
    'PRIVATE': 4,    # 私有状态
    'OVERHEAD': 5    # 置顶状态（推荐状态）
}








