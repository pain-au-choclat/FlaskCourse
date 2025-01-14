from flask import Flask
from celery import Celery
from datetime import date

from snakeeyes.blueprints.page import page
from snakeeyes.blueprints.contact import contact
from snakeeyes.extensions import debug_toolbar, mail, csrf

CELERY_TASK_LIST = [
    'snakeeyes.blueprints.contact.tasks'
]


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

    app.register_blueprint(contact)
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
    mail.init_app(app)
    csrf.init_app(app)

    return None


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
