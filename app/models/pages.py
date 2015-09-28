from app import db

class Page(db.Model):

    """页面表"""

    __tablename__ = 'pages'
    page_id = db.Column(db.Integer,primary_key=True)
    page_title = db.Column(db.Text,nullable=False)
    page_content = db.Column(db.Text)
    page_status = db.Column(db.Integer)
    page_password = db.Column(db.String)
    page_date = db.Column(db.Date,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Page % r>' % self.name


