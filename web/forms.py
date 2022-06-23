from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField

from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

class NameForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  submit = SubmitField()

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField()

class PasswordForm(FlaskForm):
  email = StringField('What\'s Your Email', validators=[DataRequired()])
  password = PasswordField('What\'s Your Password')
  submit = SubmitField('Submit')

class UserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  name = StringField('Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  role = SelectField('Role', choices=[], validate_choice=False, coerce=int)
  password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords Must Match!')])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
  favorite_color = StringField('Favorite Color')
  submit = SubmitField()

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  content = CKEditorField('Content', validators=[DataRequired()])
  slug = StringField('Slug', validators=[DataRequired()])
  submit = SubmitField('Submit')

class SearchForm(FlaskForm):
  search = StringField('Search', validators=[DataRequired()])
  submit = SubmitField()

class RoleForm(FlaskForm):
  role = StringField('Role', validators=[DataRequired()])
  submit = SubmitField()
