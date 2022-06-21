from forms import NameForm, LoginForm, PasswordForm, UserForm, PostForm
from models import db, app, Users, Posts

from dependencies import init_dependencies

from routes.users import init_user_routes
from routes.posts import init_post_routes
from routes.error_handlers import init_error_routes
from routes.default import init_default_routes

# filters: safe capitalize upper lower title trim striptags

# from the container
# flask db init -> creates migration folder
# flask db migration -m 'Initial migration'
# flask db upgrade

# from the container
# from main import db
# db.create_all()

init_dependencies()
init_user_routes()
init_post_routes()
init_error_routes()
init_default_routes()
