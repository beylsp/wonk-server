"""The application module, containing the application factory function."""
import flask
import flask_restful as rest
import resources.auth as auth
import resources.facts as facts
import settings


def create_app(config_name):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
      config_name: string, the configuration to use.

    Returns:
      The application object.
    """
    app = flask.Flask(__name__)
    app.config.from_object(settings.config[config_name])

    from wonk.login import login
    login.init_app(app)

    # facts REST api routes
    api = rest.Api(facts.facts_bp)
    api.add_resource(facts.Fact, '/r/<int:id>')
    api.add_resource(facts.FactList, '/r')
    app.register_blueprint(facts.facts_bp)

    # auth REST api routes
    api = rest.Api(auth.auth_bp)
    api.add_resource(auth.AuthProvider, '/authorize/<string:provider>')
    api.add_resource(auth.AuthCallback, '/callback/<string:provider>')
    app.register_blueprint(auth.auth_bp)

    return app
