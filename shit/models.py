from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    email = db.Column(db.String(150), unique=True)
    date_joined = db.Column(db.DateTime, default=func.now())
    salted_pass = db.Column(db.String(128))

    def __repr__(self):
        return '<Users %r>' % self.id

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey(Users.id))
    title = db.Column(db.String(30))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Posts %r>' % self.id

class Drafts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey(Users.id))
    title = db.Column(db.String(30))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Drafts %r>' % self.id

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey(Users.id))
    post = db.Column(db.Integer, db.ForeignKey(Posts.id))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Comments %r>' % self.id