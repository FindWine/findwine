# -*- coding: utf-8 -*-
import json
from django.conf import settings

from django.db.models import Func
from django.shortcuts import render
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
    return {
        c.name: {
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
        context['page_description'] = 'Find the best wines from {}'.format(self.object.name)
        if self.object.logo:
            context['page_image'] = self.object.logo.url
        return context


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


@require_GET
def error(request):
    raise Exception('Simulated Failure!')
