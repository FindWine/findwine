from django.core.management import BaseCommand
from django.urls import reverse
from integrations.data_cleanup import clean_invalid_urls


class Command(BaseCommand):
    help = 'Checks all Merchant Wines for dead links and de-activates any that are found.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help="Just print information but don't save anything",
        )

    def handle(self, *args, **options):
        cleaned_wines = clean_invalid_urls(options['debug'])
        for merchant_wine in cleaned_wines:
            print('URL for {} was not valid: {}. This can be fixed here: {}'.format(
                merchant_wine, merchant_wine.url, _get_admin_url(merchant_wine)
            ))
        if not cleaned_wines:
            print('No invalid urls found! Hooray!')


def _get_admin_url(model_instance):
    # ht: https://stackoverflow.com/a/10420949/8207
    return 'https://www.findwine.com{}'.format(reverse(
        'admin:{}_{}_change'.format(model_instance._meta.app_label, model_instance._meta.model_name),
        args=(model_instance.pk,)
    ))
