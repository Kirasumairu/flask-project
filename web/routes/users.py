from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
import os

from models import app, db, Users, Roles

from forms import NameForm, UserForm

from dependencies import get_role_id, generate_filename

def init_user_routes():
  @app.route('/user/<name>')
  def user(name):
    return render_template('user.html', user_name=name)

  @app.route('/users')
  def users():
    users = Users.query.all()
    return render_template('users.html', users=users)

  @app.route('/users/add', methods=['GET', 'POST'])
  def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
      user = Users.query.filter_by(email=form.email.data).first()
      if user is None:
        role_id = get_role_id(form.role.data)
        filename = None
        if form.profile_pic.data:
          filename = generate_filename(form.profile_pic.data.filename)
          file = request.files['profile_pic']
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        user = Users(
          username=form.username.data,
          name=form.name.data,
          email=form.email.data,
          favorite_color=form.favorite_color.data,
          password=form.password.data,
          role_id=role_id,
          profile_pic=filename,
        )
        db.session.add(user)
        db.session.commit()
      flash('User Added Successfully!')
      redirect(url_for('login'))

    roles = Roles.query.all()
    form.role.choices = [(r.id, r.role) for r in roles]
    return render_template(
      'add_user.html',
      form=form,
      name=name,
    )

  @app.route('/update/<int:id>', methods=['GET', 'POST'])
  def update(id):
    if id != current_user.id:
      return render_template('401.html')
    user = Users.query.get_or_404(id)
    form = UserForm()
    # request.form -> no data validation
    if form.validate_on_submit():
      role_id = get_role_id(form.role.data)
      user.name = form.name.data
      user.username = form.username.data
      user.email = form.email.data
      user.role_id = role_id
      user.password = form.password.data
      user.favorite_color = form.favorite_color.data
      try:
        if form.profile_pic.data:
          filename = generate_filename(form.profile_pic.data.filename)
          file = request.files['profile_pic']
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          user.profile_pic = filename

        db.session.commit()
        user = Users.query.get_or_404(id)
        
        flash('User Updated Successfully!')
        return redirect(url_for('users'))
      except Exception as e:
        flash(f'Error! Looks like there was a problem... Try again {e}')

    roles = Roles.query.all()
    form.role.choices = [(r.id, r.role) for r in roles]
    form.role.data = user.role.id
    our_users = Users.query.order_by(Users.date_added)
    return render_template(
      'update.html',
      our_users=our_users,
      form=form,
      user=user
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
