from flask import Flask
from flask_orator import Orator
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = Orator()
bcrypt = Bcrypt()
jwt = JWTManager()

from api.config import Config
from api.handlers.game import game_api
from api.handlers.user import user_api

def create_app(config_class=Config):
    """ Flask app factory. """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(game_api)
    app.register_blueprint(user_api)

    # if not app.debug and not app.testing:
        # TODO: Add logging

    return app
