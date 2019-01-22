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

    from database.models import db
    # TODO: Add testing config with the database uri in memory here!
    db.init_app(app)

    from database.models import ma
    ma.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app('config')
    app.run(debug=True)
