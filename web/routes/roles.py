from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from models import app, db, Users, Roles

from forms import RoleForm

def init_role_routes():
  @app.route('/roles')
  def roles():
    roles = Roles.query.all()
    return render_template('roles.html', roles=roles)

  @app.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
  def edit_role(id):
    form = RoleForm()
    role_to_update = Roles.query.get_or_404(id)
    if request.method == 'POST':
      role_to_update.name = request.form['role']
      try:
        db.session.commit()
        flash('User Updated Successfully!')
      except:
        flash('Error! Looks like there was a problem... Try again')

    roles = Roles.query.all()
    return render_template(
      'edit_role.html',
      roles=roles,
      form=form,
      role_to_update=role_to_update
    )

  @app.route('/roles/delete/<int:id>')
  def delete_role(id):
    role_to_delete = Roles.query.get_or_404(id)
    try:
      db.session.delete(role_to_delete)
      db.session.commit()
      flash('Role Deleted Successfully!')
    except:
      flash('Error! Looks like there was a problem... Try again')

    return redirect(url_for('roles'))

  @app.route('/roles/add', methods=['GET', 'POST'])
  def add_role():
    name = None
    form = RoleForm()
    if form.validate_on_submit():
      role = Roles.query.filter_by(role=form.role.data).first()
      if role is None:
        role = Roles(
          role=form.role.data,
        )
        db.session.add(role)
        db.session.commit()
      name = form.role.data
      form.role.data = ''
      flash('Role Added Successfully!')
      roles = Roles.query.all()
      return render_template(
        'roles.html',
        roles=roles
      )
    return render_template(
      'add_role.html',
      form=form,
      name=name,
    )
