from flask import render_template, flash, redirect, url_for
from app_blog.blog.form import FormBlogMain
from app_blog.blog.model import BlogMain
from app_blog import db
from flask_login import login_required, current_user
from app_blog.blog import blog


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