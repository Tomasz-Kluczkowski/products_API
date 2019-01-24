import pytest

from run import create_app, init_db


@pytest.fixture
def create_test_app():
    app = create_app('config.TestConfig')
    return app


@pytest.fixture
def client(create_test_app):
    return create_test_app.test_client()


@pytest.fixture
def db(create_test_app):
    _db = init_db(create_test_app)
    with create_test_app.app_context():
        _db.create_all()
        yield _db
    with create_test_app.app_context():
        _db.drop_all()
