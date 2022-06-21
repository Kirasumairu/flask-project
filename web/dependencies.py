from flask_login import LoginManager
from models import app, Users

def init_dependencies():
  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'login'

  # sets user session
  @login_manager.user_loader
  def load_user(user_id):
    return Users.query.get(int(user_id))