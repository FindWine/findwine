from django.core.management import BaseCommand

from integrations.cybercellar import CYBERCELLAR_MERCHANT_NAME
from integrations.port2port import PORT2PORT_MERCHANT_NAME
from integrations.vinoteque import VINOTEQUE_MERCHANT_NAME
from integrations.winecellar import WINECELLAR_MERCHANT_NAME
from wine.models import MerchantWine


class Command(BaseCommand):
    help = "Hides all wines that don't have feeds by setting them to 'unavailable'."

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help="Just print information but don't save anything",
        )

    def handle(self, *args, **options):
        merchants_with_feeds = [
            CYBERCELLAR_MERCHANT_NAME,
            PORT2PORT_MERCHANT_NAME,
            VINOTEQUE_MERCHANT_NAME,
            WINECELLAR_MERCHANT_NAME,
        ]
        queryset = MerchantWine.objects.filter(
            available=True
        ).exclude(
            merchant__name__in=merchants_with_feeds
        ).order_by('merchant__name')
        for merchant_wine in queryset:
            print('disabliing availability for {}: {}'.format(merchant_wine.merchant, merchant_wine.wine_vintage))
            if not options['debug']:
                merchant_wine.available = None
                merchant_wine.save()
