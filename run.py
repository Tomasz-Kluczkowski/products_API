from flask import Flask


def create_app(config_file: str) -> Flask:
    """
    App factory function.
    :return: app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_file)

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


def init_db(app):
    from database.models import db
    db.init_app(app)
    return db


if __name__ == '__main__':
    app = create_app('config')
    init_db(app)
    app.run(debug=True)
