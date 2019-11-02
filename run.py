from celery import Celery
from easy_profile import EasyProfileMiddleware
from flask import Flask


def create_app(config_file: str) -> Flask:
    """
    App factory function.
    :return: app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_file)
    app.wsgi_app = EasyProfileMiddleware(app.wsgi_app)
    return app


def init_db(app):
    from database.models import db
    db.init_app(app)
    return db


def register_blueprints(app):
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_app('config')
init_db(app)
celery = make_celery(app)

if __name__ == '__main__':
    register_blueprints(app)
    app.run(debug=True)
