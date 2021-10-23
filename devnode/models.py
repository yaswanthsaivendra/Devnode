from enum import unique
from devnode import db, app
from flask_login import UserMixin
from devnode import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    profile_image_file = db.Column(db.String(20), nullable=False, default='default_profile_pic.jpg')
    cover_image_file = db.Column(db.String(20), nullable=False, default='default_cover_pic.jpg')
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    about = db.Column(db.Text, nullable=False, default='Devnode Member')
    designation = db.Column(db.String(100), nullable=False, default='Devnode Member')
    branch = db.Column(db.String(100), default=None)
    year = db.Column(db.Integer,default=None)
    discord_id = db.Column(db.String(120), unique=True)
    twitter_id = db.Column(db.String(120), unique=True)
    github_id = db.Column(db.String(120), unique=True)
    linkedin_id = db.Column(db.String(120), unique=True)


    def get_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    def __repr__(self):
        return f"User'{self.username}', '{self.email}'"