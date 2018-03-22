import traceback
from celery import shared_task
import celery
from django.core.mail import mail_admins
from integrations import port2port, cybercellar


class NotifyFailTask(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        tb = traceback.format_exc()
        mail_admins('celery task failed! {}'.format(exc), 'Stack Trace\n\n{}'.format(tb))


@shared_task(base=NotifyFailTask)
def cleanup_dead_links_task():
    from integrations.data_cleanup import clean_invalid_urls_and_notify
    clean_invalid_urls_and_notify(debug=False)


@shared_task(base=NotifyFailTask)
def port2port_update_task():
    port2port.update_all()


@shared_task(base=NotifyFailTask)
def cybercellar_update_task():
    cybercellar.update_all()


@shared_task(base=NotifyFailTask)
def fail_task():
    raise Exception("Testing failure from background jobs.")
