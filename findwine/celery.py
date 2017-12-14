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
        from integrations.tasks import cleanup_dead_links_task
    except Exception:
        # fail hard if something went wrong bootsrapping the tasks
        traceback.print_exc()
        sys.exit()

    seconds_in_a_day = 60 * 60 * 24
    sender.add_periodic_task(seconds_in_a_day, cleanup_dead_links_task.s(),
                             name='De-activate wines pointing at dead links.')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


