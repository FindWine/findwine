from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_GET

from clickthrough.models import Clickthrough
from partners.models import Partner
from wine.models import MerchantWine


@require_GET
def buy_wine(request, slug):
    source = request.GET.get('from', '')
    if not source:
        return HttpResponseBadRequest('"source" parameter is required.')
    merchant = request.GET.get('merchant', '')
    if not merchant:
        return HttpResponseBadRequest('"merchant" parameter is required.')
    try:
        merchant_id = int(merchant)
    except ValueError:
        return HttpResponseBadRequest('"merchant" must be a valid number.')
    try:
        merchant_wine = MerchantWine.objects.get(wine_vintage__slug=slug, merchant__id=merchant_id)
    except MerchantWine.DoesNotExist:
        return HttpResponseBadRequest('The referenced wine and merchant combination could not be found.')
    try:
        partner = Partner.objects.get(slug=source)
    except Partner.DoesNotExist:
        return HttpResponseBadRequest('Unknown source partner ID: {}!'.format(source))

    Clickthrough.objects.create(partner=partner, merchant_wine=merchant_wine)
    params = {'findwine_partner_name': partner.slug}
    return HttpResponseRedirect(merchant_wine.get_url(params))
