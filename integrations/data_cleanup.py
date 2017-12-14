import requests
from wine.models import MerchantWine


def clean_invalid_urls(debug=False):
    updated_merchants = []
    for merchant_wine in MerchantWine.objects.filter(available=True):
        if not url_is_valid(merchant_wine.url):
            if not debug:
                merchant_wine.available = False
                merchant_wine.save()
            updated_merchants.append(merchant_wine)

    return updated_merchants


def url_is_valid(url):
    r = requests.get(url)
    return r.status_code == 200
