from devtools import debug

from database.models import User
from run import celery


@celery.task
def print_hello():
    users = User.query.all()
    debug(users)
