from flask import render_template, flash, redirect, url_for, request
from app_blog.blog.form import FormBlogMain, FormBlogPost, FormBlogCategory, FormDeleteCategory
from app_blog.blog.model import BlogMain, BlogPost, BlogCategory
from app_blog import db
from flask_login import login_required, current_user
from app_blog.blog import blog
from datetime import datetime
from slugify import slugify


# 建立書籍
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


# 分類管理
@blog.route('/categoryedit', methods=['GET', 'POST'])
@login_required
def edit_category():
    form = FormBlogCategory()
    form_delete = FormDeleteCategory()

    if form.validate_on_submit():
        if request.form.get('category_create'):
            form = FormBlogCategory()
            category = BlogCategory(
                name = form.category_create.data,
            )
            db.session.add(category)
            db.session.commit()

            flash('成功建立分類')

        elif request.form.get('category_delete'):
            form_delete = FormDeleteCategory()
            category_delete = form_delete.category_delete.data
            category_delete = BlogCategory.query.filter_by(id=category_delete).first()
            db.session.delete(category_delete)
            db.session.commit()

            flash('成功刪除分類')

    categorys = BlogCategory.query.all()
    form_delete = FormDeleteCategory()
    return render_template('blog/category_edit.html', categorys=categorys, form=form, form_delete=form_delete)



# 建立文章
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