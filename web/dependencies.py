from flask_login import LoginManager
from models import app, Users, Roles

BASIC_USER_ID = 2

def init_dependencies():
  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'login'

  # sets user session
  @login_manager.user_loader
  def load_user(user_id):
    return Users.query.get(int(user_id))


def get_role_id(id):
  roles = Roles.query.all()
  return next(
    (r.id for r in roles if r.id == id),
    BASIC_USER_ID
  )