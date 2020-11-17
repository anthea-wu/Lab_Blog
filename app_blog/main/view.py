from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import main
from .form import FormUserInfo
from app_blog import db
from app_blog.author.model import UserRegister


# 首頁
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


# 修改個人資料
@main.route('/userinfo', methods=['GET', 'POST'])
@login_required
def userinfo():
    form = FormUserInfo()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.add(current_user)
        db.session.commit()
        flash('個人資料更新成功')
        return redirect(url_for('main.index'))
    form.about_me.data = current_user.about_me
    form.location.data = current_user.location
    return render_template('member/userinfo.html', form=form)


# 展示個人資料
@main.route('/userinfo/<username>')
def show_uesrinfo(username):
    user = UserRegister.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('member/showUserinfo.html', user=user)