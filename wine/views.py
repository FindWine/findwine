# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
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
@login_required
def price_widget_test(request):
    return render(request, 'wine/price_widget_test.html')


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
