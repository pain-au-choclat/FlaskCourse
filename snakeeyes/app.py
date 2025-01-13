from flask import Flask
from datetime import date

from snakeeyes.blueprints.page import page
from snakeeyes.extensions import debug_toolbar


def create_app(settings_override=None):

    # Create a Flask application using the app factory pattern.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    # inject current year into context to be accessed by the layout template
    @app.context_processor
    def inject_today_date():
        return dict(today_date=date.today().year)

    app.register_blueprint(page)
    extensions(app)
    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)

    return None
