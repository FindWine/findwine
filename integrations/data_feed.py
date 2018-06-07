from collections import namedtuple

from decimal import Decimal

from integrations.util import notify_data_team
from wine.models import Merchant, MerchantWine

WINE_DATA_ATTRIBUTES = (
    "id",
    "name",
    "url",
    "price",
    "stock_amount",
    "merchant_name",
)


class WineData(namedtuple('WineData', WINE_DATA_ATTRIBUTES)):
    # https://stackoverflow.com/a/16721002/8207
    __slots__ = ()

    def __new__(cls, **kwargs):
        new_kwargs = {
            v: None for v in WINE_DATA_ATTRIBUTES
        }
        new_kwargs.update(kwargs)
        return super(WineData, cls).__new__(cls, **new_kwargs)

    def __str__(self):
        return '{} ({}, {})'.format(self.name, self.id, self.url)

    @property
    def merchant(self):
        try:
            return Merchant.objects.get(name=self.merchant_name)
        except Merchant.DoesNotExist:
            return None


def process_wine_feed(merchant, all_wine_datas, custom_processor=None, debug=False):
    results = {}
    found = set()
    skipped = []
    not_found = []
    # first pass - update everything in the feed
    for wine_data in all_wine_datas:
        wine, work_done = apply_update(wine_data, custom_processor, debug)
        if wine is not None:
            found.add(wine.pk)
            if work_done:
                results[wine] = work_done
            else:
                skipped.append(wine)
        else:
            not_found.append(wine_data)

    # second pass - update all available wines that no longer show up in the feed
    for existing_wine in MerchantWine.objects.filter(merchant=merchant, available=True):
        if existing_wine.pk not in found:
            existing_wine.available = False
            results[existing_wine] = ['Set available to False because it was missing from the feed.']
            if not debug:
                existing_wine.save()

    subject, pretty_results = _get_printed_results(merchant, results, skipped, not_found)
    if debug:
        print(subject)
        print(pretty_results)
    else:
        notify_data_team(subject, pretty_results)


def apply_update(wine_data, custom_processor=None, debug=False):
    wine = get_wine_for_data(wine_data)
    work_done = []
    if wine:
        if wine.external_id != wine_data.id:
            if wine.external_id:
                work_done.append('Changed external ID from {} to {}'.format(wine.external_id, wine_data.id))
            else:
                work_done.append('Added external ID {}'.format(wine_data.id))
            wine.external_id = wine_data.id
        if wine_data.url and wine.url != wine_data.url:
            work_done.append('Changed URL from {} to {}'.format(wine.url, wine_data.url))
            wine.url = wine_data.url

        is_available = bool(wine_data.stock_amount and wine_data.stock_amount != '0')
        if wine.available != is_available:
            wine.available = is_available
            work_done.append('Set available to {} based on a stock of {}'.format(is_available,
                                                                                 wine_data.stock_amount))
        price = Decimal(wine_data.price) if wine_data.price else None
        if price and wine.price != price:
            work_done.append('Changed price from {} to {}'.format(wine.price, price))
            wine.price = price

        if custom_processor is not None:
            custom_processor(wine_data, wine, work_done)

        if work_done and not debug:
            wine.save()
    return wine, work_done


def get_wine_for_data(wine_data):
    assert wine_data.merchant is not None
    try:
        return MerchantWine.objects.get(merchant=wine_data.merchant, external_id=wine_data.id)
    except MerchantWine.DoesNotExist:
        try:
            return MerchantWine.objects.get(merchant=wine_data.merchant, url=wine_data.url)
        except MerchantWine.DoesNotExist:
            return None
    except MerchantWine.MultipleObjectsReturned:
        message = "Failed to update wine {} because it had multiple matches for merchant {} and external ID {}".format(
            wine_data.name, wine_data.merchant, wine_data.id
        )
        notify_data_team("Skipping wine update for invalid data", message)
        return None


def _get_printed_results(merchant, results, skipped, not_found):
    total_number_processed = len(results) + len(skipped) + len(not_found)
    subject = 'Successfully processed {}/{} results from {} Feed'.format(len(results),
                                                                         total_number_processed,
                                                                         merchant.name)
    body = '{updated}\n{skipped}\n{missing}'.format(
        updated='\nApplied the following {} updates: \n{}'.format(
            len(results),
            '\n'.join([_update_to_result(wine, work_done) for wine, work_done in results.items()])
        ),
        skipped='\nNo updates applied to {} wines:\n{}'.format(
            len(skipped),
            '\n'.join(['\t{}'.format(w) for w in skipped])
        ),
        missing='\n{} wines were not found in FindWine database:\n{}'.format(
            len(not_found),
            '\n'.join(['\t{}'.format(w) for w in not_found])
        )
    )
    return subject, body


def _update_to_result(wine, work_done):
    return '\t{} ({})\n{}'.format(wine, wine.url, '\n'.join(['\t\t{}'.format(w) for w in work_done]))


def shared_element_to_data(feed_item, attribute_map, merchant_name):
    vals = {
        elem_id: feed_item.find(elem_name).text
        for elem_name, elem_id in attribute_map.items()
    }
    vals['merchant_name'] = merchant_name
    return WineData(**vals)
