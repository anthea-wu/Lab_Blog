from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators, TextAreaField


class FormBlogMain(Form):
    blog_name = StringField('書籍', validators=[
        validators.DataRequired(),
        validators.Length(1,30)
    ])

    blog_descri = TextAreaField('描述', validators=[
        validators.Length(0, 300)
    ])

    submit = SubmitField('建立文章')