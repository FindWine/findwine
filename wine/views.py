# -*- coding: utf-8 -*-
import json
from django.conf import settings

from django.db.models import Func
from django.shortcuts import render
from django.templatetags.static import static
from django.utils.text import slugify
from django.views import generic
from django.views.decorators.http import require_GET

from .models import WineVintage, Producer, Category


class IndexView(generic.ListView):
    template_name = 'wine/index.html'
    context_object_name = 'winevintage_list'

    def get_queryset(self):
        """Return the first 500 wine vintages ordered by name."""
        return WineVintage.objects.all()[:500]


@require_GET
def search(request):
    category_list = list(Category.objects.values_list('name', flat=True))
    category_map = _build_category_metadata()
    return render(request, 'wine/search.html', {
        'categories': json.dumps(category_list),
        'category_mapping': json.dumps(category_map),
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


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


@require_GET
def error(request):
    raise Exception('Simulated Failure!')
