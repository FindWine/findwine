from __future__ import absolute_import, unicode_literals
import os
import traceback
from celery import Celery

# set the default Django settings module for the 'celery' program.
import sys

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findwine.settings')

app = Celery('findwine')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    seconds_in_a_day = 60 * 60 * 24
    sender.add_periodic_task(seconds_in_a_day, cleanup_dead_links_task_wrapper.s(),
                             name='De-activate wines pointing at dead links.')
    # should run just after 11:00, 19:00, and 0:00 SAST (which is those numbers UTC)
    port2port_schedule = crontab(hour='9,17,22', minute=15, day_of_week='*')
    sender.add_periodic_task(port2port_schedule, port2port_update_task_wrapper.s(),
                             name='Update data based on port2port feed.')
    cybercellar_schedule = crontab(hour='22', minute=20, day_of_week='*')
    sender.add_periodic_task(cybercellar_schedule, cybercellar_update_task_wrapper.s(),
                             name='Update data based on cybercellar feed.')


@app.task
def cleanup_dead_links_task_wrapper():
    # this is very weird and confusing https://stackoverflow.com/a/46965132/8207
    try:
        from integrations.tasks import cleanup_dead_links_task
    except Exception:
        # fail hard if something went wrong bootsrapping the tasks
        traceback.print_exc()
        sys.exit()
    cleanup_dead_links_task()


@app.task
def port2port_update_task_wrapper():
    from integrations.tasks import port2port_update_task
    port2port_update_task()


@app.task
def cybercellar_update_task_wrapper():
    from integrations.tasks import cybercellar_update_task
    port2port_update_task()


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
