from models import app
from flask import render_template

def init_error_routes():
  @app.errorhandler(401)
  def user_not_authorized(e):
    return render_template('401.html'), 404

def init_error_routes():
  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404

  @app.errorhandler(500)
  def internal_error(e):
    return render_template('500.html'), 500