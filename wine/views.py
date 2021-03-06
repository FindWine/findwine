# -*- coding: utf-8 -*-
import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.views.decorators.http import require_GET

from wine.context_processors import absolute_url
from .models import WineVintage, Producer, Category
from integrations.tasks import fail_task


@require_GET
def search(request):
    category_list = list(Category.objects.values_list('name', flat=True))
    category_map = _build_category_metadata()
    return render(request, 'wine/search.html', {
        'categories': json.dumps(category_list),
        'category_mapping': json.dumps(category_map),
    })


@require_GET
def search_by_name(request):
    return render(request, 'wine/search_by_name.html', {
    })


def _build_category_metadata():
    """
    Creates a data structure mapping categories to all subcategories they contain.

    Used in the search dropdowns.
    """

    def _get_image_id(category):
        # todo: update this when we have images or remove it
        CATEGORY_IMAGE_MAP = {
            'dessert': 'port',
        }
        default_id = slugify(category.name)
        return CATEGORY_IMAGE_MAP.get(default_id, default_id)

    def _get_image_path(category):
        return static('/wine/images/SVGs/{}.svg'.format(_get_image_id(category)))

    def _get_selected_image_path(category):
        return static('/wine/images/SVGs/{}-c.svg'.format(_get_image_id(category)))

    return {
        c.name: {
            'id': slugify(c.name),
            'image': _get_image_path(c),
            'selected_image': _get_selected_image_path(c),
            'subcategories': [sc.name for sc in c.subcategory_set.all()]
        } for c in Category.objects.select_related()
    }


class WineDetailView(generic.DetailView):
    model = WineVintage
    template_name = 'wine/wine_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WineDetailView, self).get_context_data(**kwargs)
        # social/meta stuff
        context['page_title'] = self.object.long_name
        context['page_description'] = 'Find the best place to buy {}'.format(self.object.long_name)
        if self.object.image_pack_shot:
            context['page_image'] = self.object.image_pack_shot.url
        return context


class ProducerDetailView(generic.DetailView):
    model = Producer
    template_name = 'wine/producer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProducerDetailView, self).get_context_data(**kwargs)
        # social/meta stuff
        context['page_title'] = self.object.name
        context['page_description'] = 'Find great wine from {}'.format(self.object.name)
        if self.object.logo:
            context['page_image'] = self.object.logo.url
        return context


@require_GET
def price_widget_test(request):
    wine_vintage_with_nothing = WineVintage.objects.annotate(
        merchant_count=Count('merchantwine')
    ).filter(merchant_count=0).first()
    wine_vintage_with_many = WineVintage.objects.annotate(
        merchant_count=Count(
            'merchantwine',
            # this only works in django 2.0
            # filter=Q(merchantwine__available=True)
        )
    ).filter(merchant_count__gte=4)

    # todo: this is probably a little slow / ineffecient but hard to do in the DB until django 2.0
    wine_vintage_with_one = wine_vintage_with_two_or_more = None
    for wv in wine_vintage_with_many.prefetch_related('merchantwine_set'):
        if wine_vintage_with_two_or_more and wine_vintage_with_one:
            break
        if wine_vintage_with_two_or_more is None and wv.merchantwine_set.filter(available=True).count() > 1:
            wine_vintage_with_two_or_more = wv
        if wine_vintage_with_one is None and wv.merchantwine_set.filter(available=True).count() == 1:
            wine_vintage_with_one = wv

    assert wine_vintage_with_two_or_more, 'no wine with 2 or more available merchants found'
    assert wine_vintage_with_one, 'no wine with 1 merchant found'
    return render(request, 'wine/price_widget_test.html', context={
        'wine_vintage_with_nothing': wine_vintage_with_nothing,
        'wine_vintage_with_one': wine_vintage_with_one,
        'wine_vintage_with_two_or_more': wine_vintage_with_two_or_more,
    })


@require_GET
def error(request):
    raise Exception('Simulated Failure!')


@require_GET
def celery_error(request):
    fail_task.delay()
    return HttpResponse('Triggered a celery task that should fail.')


@require_GET
def sitemap(request):
    lines = []
    for producer in Producer.objects.all():
        lines.append(absolute_url(reverse('wine:producer_detail_by_slug', args=[producer.slug])))
    for wine_vintage in WineVintage.objects.all():
        lines.append(absolute_url(reverse('wine:wine_detail_by_slug', args=[wine_vintage.slug])))
    return HttpResponse('\n'.join(lines), content_type='text/plain')
