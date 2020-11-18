from app_blog import app, db, login_manager
from app_blog.author import author
from flask import render_template, flash, redirect, url_for, request, redirect, session
from app_blog.author.model import UserRegister
from app_blog.author.form import FormRegister, FormLogin, FormChangePWD, FormResetPWD_Mail, FormResetPWD
from app_blog.sendemail import send_mail
from flask_login import login_user, login_required, current_user, logout_user


# 首頁
# main


# 註冊
@author.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.create_confirm_token()

        send_mail(
            sender='陌上花開',
            recipients=[user.email],
            subject='啟用帳號',
            template='mail/welcome',
            mailtype='html',
            user=user,
            token=token
        )

        return render_template('register/successR.html')
    
    return render_template('register/register.html', form=form)


# 使用者認證
@author.route('/user_confirm/<token>')
def user_confirm(token):
    user = UserRegister()
    data = user.validate_confirm_token(token)
    if data:
        user = UserRegister.query.filter_by(id=data.get('userID')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()
        return render_template('register/successT.html')
    else:
        return render_template('register/failT.html')


# 登入
@author.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if current_user.is_authenticated:
        flash('你已經登入過帳號了')
        return redirect(url_for('main.index'))
    else:
        if form.validate_on_submit():
            user = UserRegister.query.filter_by(email=form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    session.permanent = True
                    login_user(user, form.remember_me.data)
                    next = request.args.get('next')
                    return redirect(next) if next else redirect(url_for('main.index'))
                else:
                    flash('錯誤的E-mail或密碼')
            else:
                flash('錯誤的E-mail或密碼')
    return render_template('login/login.html', form=form)


# 登出
@author.route('/logout')
@login_required
def logout():
    logout_user()
    flash('帳號已登出')
    return redirect(url_for('author.login'))


# 會員資料
# person


# 確認帳號啟用狀態
@author.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirm and request.endpoint not in ['author.re_userconfirm', 'author.logout', 'author.user_confirm', 'main.index'] and request.endpoint!='static' :
        flash('你的帳號還沒有啟用')
        return render_template('register/unactivate.html')


# 重新寄送認證email
@author.route('/re_userconfirm')
@login_required
def re_userconfirm():
    token = current_user.create_confirm_token()
    send_mail(
        sender='陌上花開',
        recipients=[current_user.email],
        subject='啟用帳號',
        template='mail/welcome',
        mailtype='html',
        user=current_user,
        token=token
    )
    flash('請確認你的註冊信箱，點擊網址來啟用帳號')
    return redirect(url_for('main.index'))


# 更新密碼
@author.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    form = FormChangePWD()
    if form.validate_on_submit():
        if current_user.check_password(form.password_old.data):
            current_user.password = form.password_new.data
            db.session.add(current_user)
            db.session.commit()
            flash('密碼變更成功！請重新登入')
            return redirect(url_for('author.logout'))
        else:
            flash('錯誤的舊密碼')
    return render_template('member/changePWD.html', form = form)


# 申請重設密碼
@author.route('/resetpwd', methods=['GET', 'POST'])
def resetpwd():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = FormResetPWD_Mail()
    if form.validate_on_submit():
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            token = user.create_confirm_token()
            send_mail(
                sender='陌上花開',
                recipients=[user.email],
                subject='重設密碼',
                template='mail/resetPWD',
                mailtype='html',
                user=current_user,
                token=token
            )
            flash('重設密碼的email已寄出，請檢查你註冊的email信箱')
            return redirect(url_for('author.login'))
    return render_template('member/resetPWDmail.html', form=form)


# 重設密碼
@author.route('/resetPWD_recive/<token>', methods=['GET', 'POST'])
def resetPWD_recive(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    
    form = FormResetPWD()
    if form.validate_on_submit():
        user = UserRegister()
        data = user.validate_confirm_token(token)
        print(data)
        if data:
            
            user = UserRegister.query.filter_by(id=data.get('userID')).first()
            if user:
                user.password = form.password.data
                db.session.commit()
                flash('密碼重設成功！')
                return redirect(url_for('author.login'))
            else:
                flash
                flash('搜尋不到用戶名稱')
                return redirect(url_for('main.index'))
        else:
            flash('認證錯誤！請重新申請一次並在10分鐘內設定新密碼')
            return redirect(url_for('main.index'))
    return render_template('member/resetPWD.html', form=form)


@login_manager.user_loader
def load_user(userID):
    from app_blog.author.model import UserRegister
    user = UserRegister.query.filter_by(id=userID).first()
    if user:
        return user
    return None