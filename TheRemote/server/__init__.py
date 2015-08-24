from flask import Flask
from flask.ext.login import LoginManager

from theremote.database.models import User

app = Flask(__name__)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)

app.run(port=3333)