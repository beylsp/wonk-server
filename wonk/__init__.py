"""The application module, containing the application factory function."""
from flask import Flask
from flask_restful import Api
from wonk import settings
from wonk.resources.v1 import auth


def create_app(config_name):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
      config_name: string, the configuration to use.

    Returns:
      The application object.
    """
    app = Flask(__name__)
    app.config.from_object(settings.config[config_name])

    from wonk.models.users import db
    db.init_app(app)

    # authentication REST api v1 routes
    api = Api(auth.blueprint)
    api.add_resource(auth.Login, '/rest/auth/v1/login/')
    api.add_resource(auth.Logout, '/rest/auth/v1/logout/')
    app.register_blueprint(auth.blueprint)

    return app
