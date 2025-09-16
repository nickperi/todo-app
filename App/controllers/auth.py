from flask import redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User
from App.database import db

def login(username, password):
  try:
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
      return create_access_token(identity=user.username)
  except Exception as e:
    db.session.rollback()
    return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = User.query.filter_by(username=identity).one_or_none()
    if user:
        return user.username
    return None
  
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    response = redirect(url_for('index_views.index_page'))  
    return response

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).first()
  return jwt

  


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          identity = get_jwt_identity()
          current_user = User.query.filter_by(username=identity)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)
