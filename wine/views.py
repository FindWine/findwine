# -*- coding: utf-8 -*-
import json

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
    category_map = _build_category_subcategory_mapping()
    return render(request, 'wine/search.html', {
        'categories': json.dumps(category_list),
        'category_mapping': json.dumps(category_map),
    })


def _build_category_subcategory_mapping():
    """
    Creates a data structure mapping categories to all subcategories they contain.

    Used in the search dropdowns.
    """
    return {
        c.name: [sc.name for sc in c.subcategory_set.all()] for c in Category.objects.select_related()
    }


class WineDetailView(generic.DetailView):
    model = WineVintage
    template_name = 'wine/wine_detail.html'


class ProducerDetailView(generic.DetailView):
    model = Producer
    template_name = 'wine/producer_detail.html'


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


@require_GET
def error(request):
    raise Exception('Simulated Failure!')
