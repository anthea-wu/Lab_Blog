from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Command, Shell
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from datetime import timedelta
from flask import Blueprint

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'author.login'
login_manager.login_message = '請登入系統來檢視這個頁面'
login_manager.session_protection = "strong"

from .author import author
app.register_blueprint(author, url_prefix='/author')

from .person import person
app.register_blueprint(person, url_prefix='/person')

from .main import main
app.register_blueprint(main, url_prefix='')