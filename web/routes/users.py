from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from models import app, db, Users

from forms import NameForm, UserForm

def init_user_routes():
  @app.route('/user/<name>')
  def user(name):
    return render_template('user.html', user_name=name)

  @app.route('/update/<int:id>', methods=['GET', 'POST'])
  def update(id):
    if id != current_user.id:
      return render_template('401.html')
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
      user_to_update.name = request.form['name']
      user_to_update.username = request.form['username']
      user_to_update.email = request.form['email']
      user_to_update.password = request.form['password']
      user_to_update.favorite_color = request.form['favorite_color']
      try:
        db.session.commit()
        flash('User Updated Successfully!')
      except:
        flash('Error! Looks like there was a problem... Try again')

    our_users = Users.query.order_by(Users.date_added)
    return render_template(
      'update.html',
      our_users=our_users,
      form=form,
      user_to_update=user_to_update
    )

  @app.route('/delete/<int:id>')
  @login_required
  def delete(id):
    if id != current_user.id:
      return render_template('401.html')

    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
      db.session.delete(user_to_delete)
      db.session.commit()
      flash('User Deleted Successfully!')
    except:
      flash('Error! Looks like there was a problem... Try again')

    our_users = Users.query.order_by(Users.date_added)
    return render_template(
      'add_user.html',
      form=form,
      name=name,
      our_users=our_users
    )

  @app.route('/users/add', methods=['GET', 'POST'])
  def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
      user = Users.query.filter_by(email=form.email.data).first()
      if user is None:
        user = Users(
          username=form.username.data,
          name=form.name.data,
          email=form.email.data,
          favorite_color=form.favorite_color.data,
          password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
      name = form.name.data
      form.name.data = ''
      form.username.data = ''
      form.email.data = ''
      form.password.data = ''
      form.favorite_color.data = ''
      flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.date_added)
    return render_template(
      'add_user.html',
      form=form,
      name=name,
      our_users=our_users
    )