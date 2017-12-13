from django.urls import reverse
import requests
from wine.context_processors import absolute_url
from wine.models import MerchantWine


def clean_invalid_urls(debug=False):
    for merchant_wine in MerchantWine.objects.filter(available=True):
        if not url_is_valid(merchant_wine.url):
            if not debug:
                merchant_wine.available = False
                merchant_wine.save()
            else:
                print('URL for {} was not valid: {}. This can be fixed here: {}'.format(
                    merchant_wine, merchant_wine.url, _get_admin_url(merchant_wine)
                ))


def url_is_valid(url):
    r = requests.get(url)
    return r.status_code == 200


def _get_admin_url(model_instance):
    # ht: https://stackoverflow.com/a/10420949/8207
    return 'https://www.findwine.com{}'.format(reverse(
        'admin:{}_{}_change'.format(model_instance._meta.app_label, model_instance._meta.model_name),
        args=(model_instance.pk,)
    ))
