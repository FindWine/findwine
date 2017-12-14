from celery import shared_task


@shared_task
def cleanup_dead_links_task():
    from integrations.data_cleanup import clean_invalid_urls_and_notify
    clean_invalid_urls_and_notify(debug=False)
