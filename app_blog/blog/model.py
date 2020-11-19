from app_blog import db
from datetime import datetime


class BlogMain(db.Model):
    __tablename__ = 'BlogMains'
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(30), nullable=False)
    blog_descri = db.Column(db.String(200))
    blog_create_date = db.Column(db.DateTime(), default=datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('UserRegister.id'))
    post = db.relationship('BlogPost', backref='blogs', lazy='dynamic')

    def __init__(self, blog_name, blog_descri, author):
        self.blog_name = blog_name
        self.blog_descri = blog_descri
        self.author = author

    def __repr__(self):
        return 'Blog: {}, Author: {}'.format(self.blog_name, self.author)


class BlogPost(db.Model):
    __tablename__ = 'BlogPosts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text)
    category = db.Column(db.Integer, db.ForeignKey('BlogCategorys.id'))
    author = db.Column(db.Integer, db.ForeignKey('UserRegister.id'))
    blog = db.Column(db.Integer, db.ForeignKey('BlogMains.id'))
    create_date = db.Column(db.DateTime(), default=datetime.utcnow())
    edit_date = db.Column(db.DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
    slug = db.Column(db.String(256), unique=True)
    flag = db.Column(db.Boolean, default=True)
    categorys = db.relationship('BlogCategory', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, author, blog, slug=None):
        self.title = title
        self.body = body
        self.category = category
        self.author = author
        self.blog = blog
        self.slug = slug

    def __repr__(self):
        return 'Post: {}'.format(self.title)


class BlogCategory(db.Model):
    __tablename__ = 'BlogCategorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Category: {}'.format(self.name)