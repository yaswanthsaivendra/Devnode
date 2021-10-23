from enum import unique
from devnode import db, app
from flask_login import UserMixin
from devnode import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

association_table = db.Table('association',
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

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
    skills = db.relationship('Skill', secondary=association_table, lazy='subquery',
        backref=db.backref('users_associated', lazy=True))
    posts = db.relationship('Post', backref='author', lazy=True)

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

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content= db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(120), nullable=False)
    last_date = db.Column(db.String(80), nullable=False)
    persons_required = db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User'{self.title}', '{self.date_posted}'"