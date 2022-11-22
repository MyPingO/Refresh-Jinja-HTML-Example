from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    create_database_if_not_exist(app)
    from website.database import User, Numbers


    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))    


    return app

def create_database_if_not_exist(app):
    if not Path('website/' + database_name).exists():
        db.create_all(app=app)
        print('Created Database!')