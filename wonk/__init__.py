"""The application module, containing the application factory function."""
from flask import Flask
from flask_restful import Api
from wonk.resources import facts
from wonk.resources import auth
from wonk.resources import token

import settings


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

    from wonk.login import login
    login.init_app(app)

    from wonk.db import db
    db.init_app(app)

    # facts REST api routes
    api = Api(facts.facts_bp)
    api.add_resource(facts.Fact, '/r/<int:id>/')
    api.add_resource(facts.FactList, '/r/')
    app.register_blueprint(facts.facts_bp)

    # oauth REST api routes
    api = Api(auth.oauth_bp)
    api.add_resource(auth.OAuthProvider, '/oauth/<string:provider>/')
    api.add_resource(auth.OAuthCallback, '/oauthcb/<string:provider>/')
    app.register_blueprint(auth.oauth_bp)

    # token REST api routes
    api = Api(token.token_bp)
    api.add_resource(token.TokenProvider, '/token/')
    app.register_blueprint(token.token_bp)

    return app
