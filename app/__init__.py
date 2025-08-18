# this is the init for the whole program.
# for right now it's not very robust, but its mainly b/c don't have many extensions.

from flask import Flask
from .ext import mongo, limiter
from .routes.main import main
from .routes.redirect import redir
from .routes.errors import errors, register

# how we build the app, see wsgi.py
def create_app(config_object="config.Config") -> Flask:
    # create da flask app
    app: Flask = Flask(__name__)
    app.config.from_object(config_object)

    # then init mongo and limiter
    mongo.init_app(app)
    limiter.init_app(app)

    # finally register blueprints
    app.register_blueprint(main)
    app.register_blueprint(redir)
    app.register_blueprint(errors)

    # and the error handler (hid it behind a function to make it cleaner)
    register(app)

    # and send er on back private
    return app