from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from models import app, db, Posts

from forms import PostForm

def init_post_routes():
  @app.route('/add-post', methods=['GET', 'POST'])
  def add_post():
    form = PostForm()
    if form.validate_on_submit():
      author_id = current_user.id
      post = Posts(
        title=form.title.data,
        content=form.content.data,
        author_id=author_id,
        slug=form.slug.data,
      )
      form.title.data = ''
      form.content.data = ''
      form.slug.data = ''
      db.session.add(post)
      db.session.commit()
      flash('Blog Post Submitted Successfully!')
      return redirect(url_for('posts'))
    return render_template('add_post.html', form=form)

  @app.route('/posts')
  def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

  @app.route('/posts/<int:id>')
  def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

  @app.route('/posts/edit/<int:id>', methods=['GET','POST'])
  @login_required
  def edit_post(id):
    post = Posts.query.get_or_404(id)
    if post.author.id != current_user.id:
      return render_template('401.html')
    form = PostForm()
    if form.validate_on_submit():
      post.title = form.title.data
      post.slug = form.slug.data
      post.content = form.content.data
      db.session.add(post)
      db.session.commit()
      flash('Post Has Been Updated!')
      return redirect(url_for('post', id=post.id))
    
    form.title.data = post.title
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

  @app.route('/posts/delete/<int:id>')
  @login_required
  def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    if post_to_delete.author.id != current_user.id:
      return render_template('401.html')
    try:
      db.session.delete(post_to_delete)
      db.session.commit()
      flash('Post Deleted Successfully!')
    except:
      flash('Error! Looks like there was a problem... Try again')

    posts = Posts.query.order_by(Posts.date_posted)
    return redirect(url_for(
      'posts',
      posts=posts,
    ))
