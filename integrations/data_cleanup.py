from django.core.mail import mail_admins
import requests
from wine.models import MerchantWine
from django.urls import reverse


def clean_invalid_urls_and_notify(debug=False):
    cleaned_wines = clean_invalid_urls(debug)
    found_issues = [
        'URL for {} was not valid: {}. This can be fixed here: {}'.format(
            merchant_wine, merchant_wine.url, _get_admin_url(merchant_wine)
        )
        for merchant_wine in cleaned_wines
    ]
    if not found_issues:
        mail_admins('Merchant URL check succeeded with no issues found.', '')
    else:
        mail_admins('Merchant URL check found {} new issues.'.format(len(found_issues)), '\n'.join(found_issues))


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


def _get_admin_url(model_instance):
    # ht: https://stackoverflow.com/a/10420949/8207
    return 'https://www.findwine.com{}'.format(reverse(
        'admin:{}_{}_change'.format(model_instance._meta.app_label, model_instance._meta.model_name),
        args=(model_instance.pk,)
    ))