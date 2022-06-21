from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@mysql/users'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)

# UserMixin for the flask_login
class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(120), nullable=False, unique=True)
  name = db.Column(db.String(200), nullable=False)
  password_hash = db.Column(db.String(128))
  email = db.Column(db.String(120), nullable=False, unique=True)
  favorite_color = db.Column(db.String(120))
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  posts = db.relationship('Posts', backref='author')

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

class Posts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  content = db.Column(db.Text)
  # author = db.Column(db.String(255))
  date_posted = db.Column(db.DateTime, default=datetime.utcnow)
  slug = db.Column(db.String(255))
  author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
