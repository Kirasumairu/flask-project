from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# filters: safe capitalize upper lower title trim striptags

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@mysql/users'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from the container
# flask db init -> creates migration folder
# flask db migration -m 'Initial migration'
# flask db upgrade

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  password_hash = db.Column(db.String(128))
  email = db.Column(db.String(120), nullable=False, unique=True)
  favorite_color = db.Column(db.String(120))
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute!')

  @password.setter
  def password(self, passwd):
    self.password_hash = generate_password_hash(passwd)

  def verify_password(self, passwd):
    return check_password_hash(self.password_hash, passwd)

  def __repr__(self):
    return '<Name %r>' % self.name

# from the container
# from main import db
# db.create_all()
# 
class NameForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField()

class PasswordForm(FlaskForm):
  email = StringField('What\'s Your Email', validators=[DataRequired()])
  password = PasswordField('What\'s Your Password')
  submit = SubmitField('Submit')

class UserForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
  favorite_color = StringField('Favorite Color')
  submit = SubmitField()

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

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  form = UserForm()
  user_to_update = Users.query.get_or_404(id)
  if request.method == 'POST':
    user_to_update.name = request.form['name']
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
def delete(id):
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
        name=form.name.data,
        email=form.email.data,
        favorite_color=form.favorite_color.data,
        password=form.password.data
      )
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.name.data = ''
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

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', user_name=name)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500

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
    is_correct = check_password_hash(user.password_hash, password)

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
