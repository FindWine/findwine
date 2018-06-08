from django.core.management import BaseCommand
from integrations.vinoteque import update_all


class Command(BaseCommand):
    help = 'Imports data from the Vinoteque feed.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help="Just print information but don't save anything",
        )

    def handle(self, *args, **options):
        update_all(options['debug'])
