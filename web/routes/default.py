from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user

from models import app, db, Users

from forms import LoginForm, NameForm

def init_default_routes():
  @app.route('/')
  def index():
    first_name = 'Johnny'
    code = '<strong>This is bolded</strong>'
    favorite_pizza = ['Pineapple', 'Margarita']
    return render_template(
      'index.html',
      first_name=first_name,
      code=code,
      favorite_pizza=favorite_pizza
    )

  @app.route('/dashboard', methods=['GET', 'POST'])
  # @login_required has to be declared before the function
  @login_required
  def dashboard():
    return render_template('dashboard.html')

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    form = LoginForm()
    if form.validate_on_submit():
      user = Users.query.filter_by(username=form.username.data).first()
      if user and user.verify_password(form.password.data):
        login_user(user)
        flash('Login Successfull!')
        return redirect(url_for('dashboard'))
      else:
        flash('Something went wrong... Try again')
    return render_template('login.html', form=form)

  @app.route('/logout')
  def logout():
    logout_user()
    flash('You Have Been Logged Out!')
    return redirect(url_for('login'))

  @app.route('/favorite_pizza')
  def get_favorite_pizza():
    favorite_piza = {
      'John': 'Pepperoni',
      'Mary': 'Cheese'
    }
    return favorite_piza
    # return {'Date': datetime.today()}

  @app.route('/name', methods=['GET', 'POST'])
  def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
      name = form.name.data
      form.name.data = ''
      flash('Form Submitted Successfully')
    
    return render_template(
      'name.html', 
      name=name,
      form=form
    )

  @app.route('/test_pw', methods=['GET', 'POST'])
  def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    user = None
    is_correct = False
    form = PasswordForm()
    if form.validate_on_submit():
      email = form.email.data
      password = form.password.data

      user = Users.query.filter_by(email=email).first()
      is_correct = user.verify_password(user.password_hash, password)

      form.email.data = ''
      form.password.data = ''

    return render_template(
      'test_pw.html', 
      email=email,
      password=password,
      form=form,
      user=user,
      is_correct=is_correct
    )
