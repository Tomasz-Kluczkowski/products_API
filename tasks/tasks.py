from devtools import debug

from database.models import User
from run import celery


class PrintTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        debug('FAILED!!!!')
        debug(self.app)
        # with self.app.app_context():
        # self.app
        # with app.app_context():
        #     users = User.query.all()
        # debug(users)


@celery.task(bind=True, base=PrintTask, autoretry_for=(Exception, ), retry_kwargs={'max_retries': 2, 'countdown': 2})
def print_hello(self):
    debug('TRIGGERING EXCEPTION')
    users = User.query.all()
    debug(users)
    raise Exception
