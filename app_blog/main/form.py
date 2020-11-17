from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators, SelectField, TextAreaField


class FormUserInfo(Form):
    about_me = TextAreaField('關於我', validators=[
        validators.DataRequired()
    ])

    location = StringField('位置', validators=[
        validators.DataRequired(),
        validators.Length(1,20)
    ])

    submit = SubmitField('提交')