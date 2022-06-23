from flask_login import LoginManager
from models import app, Users, Roles
from werkzeug.utils import secure_filename
import uuid as uuid

BASIC_USER_ID = 2

def generate_filename(filename):
  return f"{uuid.uuid4()}_{secure_filename(filename)}"

def get_role_id(id):
  roles = Roles.query.all()
  return next(
    (r.id for r in roles if r.id == id),
    BASIC_USER_ID
  )


def init_dependencies():
  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'login'

  # sets user session
  @login_manager.user_loader
  def load_user(user_id):
    return Users.query.get(int(user_id))