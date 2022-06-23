from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from models import app, db, Users, Roles

from forms import NameForm, UserForm

from dependencies import get_role_id

def init_user_routes():
  @app.route('/user/<name>')
  def user(name):
    return render_template('user.html', user_name=name)

  @app.route('/users')
  def users():
    users = Users.query.all()
    return render_template('users.html', users=users)

  @app.route('/update/<int:id>', methods=['GET', 'POST'])
  def update(id):
    if id != current_user.id:
      return render_template('401.html')
    user_to_update = Users.query.get_or_404(id)
    form = UserForm()
    # request.form -> no data validation
    if form.validate_on_submit():
      role_id = get_role_id(form.role.data)
      user_to_update.name = form.name.data
      user_to_update.username = form.username.data
      user_to_update.email = form.email.data
      user_to_update.role_id = role_id
      user_to_update.password = form.password.data
      user_to_update.favorite_color = form.favorite_color.data
      try:
        db.session.commit()
        user_to_update = Users.query.get_or_404(id)
        flash('User Updated Successfully!')
        return redirect(url_for('users'))
      except:
        flash('Error! Looks like there was a problem... Try again')

    roles = Roles.query.all()
    form.role.choices = [(r.id, r.role) for r in roles]
    form.role.data = user_to_update.role.id
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

    return redirect(url_for('users'))

  @app.route('/users/add', methods=['GET', 'POST'])
  def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
      user = Users.query.filter_by(email=form.email.data).first()
      if user is None:
        role_id = get_role_id(form.role.data)
        user = Users(
          username=form.username.data,
          name=form.name.data,
          email=form.email.data,
          favorite_color=form.favorite_color.data,
          password=form.password.data,
          role_id=role_id
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
      redirect(url_for('login'))

    roles = Roles.query.all()
    form.role.choices = [(r.id, r.role) for r in roles]
    return render_template(
      'add_user.html',
      form=form,
      name=name,
    )
