from copy import copy
from django.conf import settings
from django.templatetags.static import static


def absolute_url(relative_url):
    return '{}{}'.format(settings.SITE_URL, relative_url)


def site_meta(request):
    site = copy(settings.SITE)
    site['IMAGE_URL'] = absolute_url(static(site['IMAGE']))
    site['TITLE'] = '{} - {}'.format(site['NAME'], site['SUBTITLE'])
    return {
        'site': site,
        'page_url': absolute_url(request.path),
        'page_title': '',
        'page_description': '',
        'page_image': '',
    }
