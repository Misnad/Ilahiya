from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "083f3d45cad3cde9ecf06b2fa05e4200"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
db.init_app(app)


from shit.auth import auth
from shit.views import view

app.register_blueprint(view, url_prefix='/')
app.register_blueprint(auth, url_prefix="/")


# Create Database (if dosent exist)
with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
