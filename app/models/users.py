from app import db 

class User(db.Model):

    """用户表"""

    __tablename__ = 'users'
    user_id = db.Column(db.BigInteger(20),primary_key=True)
    user_login = db.Column(db.String(60),unique=True)
    user_nicename = db.Column(db.String(50),unique=True)
    user_pass = db.Column(db.String(64))
    user_email = db.Column(db.String(100))
    user_url = db.Column(db.String(100))
    user_rule = db.Column(db.Integer(5))

    posts = db.relationship('Post',backref='users')
    pages = db.relationship('Page',backref='Users')

    def __repr__(self):
        return '<Users %r>' % self.name
