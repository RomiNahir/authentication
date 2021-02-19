import dash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
from users import db, Users as base
from config import config


app = dash.Dash(__name__,suppress_callback_exceptions=True)

app.title = 'AWS Dash Authentication Demo'

server = app.server


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# Create User class with UserMixin
class Users(UserMixin, Users):
    pass

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))