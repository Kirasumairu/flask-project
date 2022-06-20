from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# filters: safe capitalize upper lower title trim striptags

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@mysql/users'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(120), nullable=False, unique=True)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Name %r>' % self.name

# from the container
# from main import db
# db.create_all()
# 
class NameForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField()

class UserForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
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

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
  name = None
  form = UserForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      user = Users(name=form.name.data, email=form.email.data)
      db.session.add(user)
      db.session.commit()
    name = form.name.data
    form.name.data = ''
    form.email.data = ''
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
