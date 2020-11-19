from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators, TextAreaField, SelectField
from flask_login import current_user
from .model import BlogMain, BlogCategory
from sqlalchemy import text


class FormBlogMain(Form):
    blog_name = StringField('書籍', validators=[
        validators.DataRequired(),
        validators.Length(1,30)
    ])

    blog_descri = TextAreaField('描述', validators=[
        validators.Length(0, 300)
    ])

    submit = SubmitField('建立文章')


class FormBlogPost(Form):
    title = StringField('文章標題', validators=[
        validators.DataRequired(),
        validators.Length(1, 50)
    ])

    body = TextAreaField('內容', validators=[
        validators.DataRequired()
    ])

    blog = SelectField('書籍', coerce=int)
    category = SelectField('分類', coerce=int)

    submit = SubmitField('送出')

    def __init__(self):
        super(FormBlogPost, self).__init__()
        self.blog.choices = self._get_blog()
        self.category.choices = self._get_category()

    def _get_blog(self):
        obj = BlogMain.query.with_entities(BlogMain.id, BlogMain.blog_name).filter_by(author=current_user._get_current_object().id).all()
        return obj

    def _get_category(self):
        obj = BlogCategory.query.with_entities(BlogCategory.id, BlogCategory.name).all()
        return obj