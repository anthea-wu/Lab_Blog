from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app_blog.main import main
from app_blog import db
from app_blog.author.model import UserRegister


# 首頁
@main.route('/')
def index():
    return render_template('index.html')