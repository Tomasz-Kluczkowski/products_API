from celery import Celery
from devtools import debug

import time

celery_app = Celery('celery_trial', backend='rpc://', broker='pyamqp://guest@localhost//')


class BaseTask(celery_app.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        debug(task_id)
        debug(einfo)
        debug(args)
        debug(kwargs)


@celery_app.task(base=BaseTask, bind=True, name='experiments.celery_trial.add', autoretry_for=(Exception, ), retry_kwargs={'max_retries': 2, 'countdown': 2})
def add(self, x, y):
    debug('CALCULATING')
    # try:
    raise Exception
    return x + y
    # except Exception as exc:
    #     self.retry(exc=exc, max_retries=2, countdown=2)


# result = add.delay(2, 1)


# debug(result)
# debug(result.status)
# debug(result.state)
# status = result.get()
# debug(status)
