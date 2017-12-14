from django.core.management import BaseCommand
from integrations.data_cleanup import clean_invalid_urls_and_notify


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
        clean_invalid_urls_and_notify(options['debug'])
