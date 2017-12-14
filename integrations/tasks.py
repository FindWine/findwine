from celery import shared_task
from _datetime import datetime


@shared_task
def debug_task():
    print('The current time is {}'.format(datetime.now()))
