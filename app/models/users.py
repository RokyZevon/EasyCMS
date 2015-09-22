from app import db 

class Users(db.Model):
    __tablename__ = 'wp_users'
    ID = db.Column(db.BigInteger(20),primary_key=True)
    user_login = db.Column(db.String(60),unique=True)
    user_pass = db.Column(db.String(64))
    user_nicename = db.Column(db.String(50),unique=True)
    user_email = db.Column(db.String(100))
    user_url = db.Column(db.String(100))
    user_registered = db.Column(db.Date)
    user_activation_key = db.Column(db.String(60))
    user_status = db.Column(db.Integer(11))
    display_name = db.Column(db.String(250))

    def __repr__(self):
        return '<Users %r>' % self.name
