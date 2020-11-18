from app_blog import db
from datetime import datetime


class BlogMain(db.Model):
    __tablename__ = 'BlogMains'
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(30), nullable=False)
    blog_descri = db.Column(db.String(200))
    blog_create_date = db.Column(db.DateTime(), default=datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('UserRegister.id'))

    def __init__(self, blog_name, blog_descri, author):
        self.blog_name = blog_name
        self.blog_descri = blog_descri
        self.author = author

    def __repr__(self):
        return 'Blog: {}, Author: {}'.format(self.blog_name, self.author)