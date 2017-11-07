from django import template


register = template.Library()


@register.filter
def get_title(site, page_title=None):
    if page_title:
        return '{} | {}'.format(page_title, site['NAME'])
    else:
        return site['TITLE']


@register.filter
def get_description(site, page_description=None):
    return page_description or site['DESCRIPTION']


@register.filter
def get_image_url(site, page_image=None):
    return page_image or site['IMAGE_URL']
