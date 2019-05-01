import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///products.db'
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'

# API messages keys
UNKNOWN_API_KEY = 'unknown_api_key'
DUPLICATE_PRODUCT = 'duplicate_product'
PRODUCT_CREATED = 'product_created'
NO_JSON = 'no_json'
INCORRECT_DATA = 'incorrect_data'

MESSAGES = {
    UNKNOWN_API_KEY: 'Unknown API key. Please check your API key.',
    DUPLICATE_PRODUCT: 'Product already in database, use PUT or PATCH methods to amend.',
    PRODUCT_CREATED: 'Product created',
    NO_JSON: 'No JSON body supplied',
    INCORRECT_DATA: 'Incorrect product data supplied.'
}


class TestConfig:
    TESTING = True
    # in memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
