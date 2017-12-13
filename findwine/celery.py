from __future__ import absolute_import, unicode_literals
import os
import traceback
from celery import Celery

# set the default Django settings module for the 'celery' program.
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findwine.settings')

app = Celery('findwine')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        from integrations.tasks import debug_task
    except Exception:
        # fail hard if something went wrong bootsrapping the tasks
        traceback.print_exc()
        sys.exit()

    sender.add_periodic_task(1, debug_task.s(), name='Debug task to make sure things are working')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


