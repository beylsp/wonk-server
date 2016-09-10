"""The application module, containing the application factory function."""
from flask import Flask

from app.config import config
from app.views.auth import auth


def create_app(config_name):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
      config_name: string, the configuration to use.

    Returns:
      The application object.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.login import login
    login.init_app(app)

    from app.rest import rest
    rest.init_app(app)

    app.register_blueprint(auth)

    return app
