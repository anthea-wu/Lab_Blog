from flask import render_template, flash, redirect, url_for
from app_blog.blog.form import FormBlogMain, FormBlogPost
from app_blog.blog.model import BlogMain, BlogPost
from app_blog import db
from flask_login import login_required, current_user
from app_blog.blog import blog
from datetime import datetime
from slugify import slugify


@blog.route('/bookbuild', methods=['GET', 'POST'])
@login_required
def build_book():
    form = FormBlogMain()
    if form.validate_on_submit():
        blog = BlogMain(
            blog_name = form.blog_name.data,
            blog_descri = form.blog_descri.data,
            author = current_user.id
        )
        db.session.add(blog)
        db.session.commit()

        flash('成功建立書籍')

        return redirect(url_for('person.show_uesrinfo', username = current_user.username))

    return render_template('blog/book_build.html', form=form)


@blog.route('/postedit', methods=['GET', 'POST'])
@login_required
def post_edit():
    form = FormBlogPost()
    if form.validate_on_submit():
        post = BlogPost(
            title = form.title.data,
            body = form.body.data,
            category = form.category.data,
            author = current_user.id,
            blog = form.blog.data,
            slug = '{}-{}-{}-{}-{}'.format(current_user.id, datetime.now().year, datetime.now().month, datetime.now().day, slugify(form.title.data))
        )
        print(current_user._get_current_object())
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('blog.post_edit'))
    return render_template('blog/post_edit.html', form=form)