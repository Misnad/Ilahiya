from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = "kh54c#xyh*65c#@co52jbd226JUb"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
db.init_app(app)

from .views import view
app.register_blueprint(view, url_prefix='/')
from .auth import auth
app.register_blueprint(auth, url_prefix="/")

# Create Database (if dosent exist)
from .models import Users, Posts, Drafts, Comments
with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

app.run(debug=True)