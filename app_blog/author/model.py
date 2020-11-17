from app_blog import db, bcrypt, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app
from flask_login import UserMixin
from datetime import datetime

class UserRegister(UserMixin, db.Model):
    __tablename__ = 'UserRegister'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(30), unique=True, nullable=False)
    confirm = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.Text())
    location = db.Column(db.String(20))
    regist_date = db.Column(db.DateTime(), default = datetime.utcnow())
    last_login = db.Column(db.DateTime(), default = datetime.utcnow())

    @property
    def password(self):
        raise AttributeError('這是一個未加密的密碼')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def create_confirm_token(self, expires_in=600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'userID': self.id})

    def validate_confirm_token(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return data

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def create_reset_token(self, expires_in=600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps( {'resetID': self.id} )
        
    def __repr__(self):
        return '帳號：{} email：{}'.format(self.username, self.email)



#db.create_all()