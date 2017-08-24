# -*- coding: utf-8 -*-

from django.db.models import Avg, Min, Func
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_GET

from .models import WineVintage, MerchantWine, Producer, SubCategory
from .forms import BasicSearchForm, AdvancedSearchForm


class IndexView(generic.ListView):
    template_name = 'wine/index.html'
    context_object_name = 'winevintage_list'

    def get_queryset(self):
        """Return the first 500 wine vintages ordered by name."""
        return WineVintage.objects.all()[:500]

@require_GET
def search(request):
    form = BasicSearchForm()
    return render(request, 'wine/search.html', {'form': form})


def update_subcategories(request):
    category = request.GET.get('category', None)
    sub_category = list(SubCategory.objects.filter(category__name__exact=category).values('name'))
    return JsonResponse(sub_category, safe=False)


class ResultsView(generic.ListView):
    template_name = 'wine/results.html'
    context_object_name = 'results_list'
    paginate_by = 50

    def get_queryset(self):
        category = self.request.GET.get('category', '')
        sub_category = self.request.GET.get('sub_category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        #1 todo: Add country
        results_list = MerchantWine.objects.filter(
            #2 Restrict MerchantWines to those that are available
            available__exact="True",
            #3 Restrict MerchantWines to those that are above or equal to the minimum price
            price__gte=min_price,
            #4 Restrict MerchantWines to those that are below or equal to the maximum price
            price__lte=max_price,
            #5 Restrict MerchantWines to the selected category
            wine_vintage__category__name__exact=category,
        )

        #6 Restrict MerchantWines to the selected sub_category or leave if no sub_category is selected NB! UPDATE FOR MULTIPLE SELECT
        if sub_category != 'All':
            results_list = results_list.filter(wine_vintage__sub_category__name__exact=sub_category)

        #7 Restrict MerchantWines to lowest price version(s) of same wine_vintage
        wines = WineVintage.objects.distinct().filter(merchantwine__in=results_list)
        #8 Only show lowest price and add average rating
        wines = wines.annotate(
            price=Round(Min('merchantwine__price')),
            avg_rating=Round(Avg('wineaward__award__tier__normalised_rating')),

        )
        wines = wines.order_by(
            '-avg_rating', 'price'
        )
        # todo: if necessary
        # #9 Restrict MerchantWines to lowest minimum_purchase_unit of same wine_vintage, price and merchant
        # # NOT WORKING min_units = results_list.values('wine_vintage').annotate(smallest_unit=Min('minimum_purchase_unit'))
        # # NOT WORKING results_list = results_list.filter(minimum_purchase_unit__in=min_units.values('smallest_unit'))
        return wines


class WineDetailView(generic.DetailView):
    model = WineVintage
    template_name = 'wine/wine_detail.html'


class ProducerDetailView(generic.DetailView):
    model = Producer
    template_name = 'wine/producer_detail.html'


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


def AdvancedSearch(request):
    # REMOVE POST STUFF? ADD???
    if request.method == 'POST':
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            # redirect to a new URL:
            return render(request, 'wine/search.html', {'form': form})
    else:
        form = AdvancedSearchForm()
        return render(request, 'wine/search.html', {'form': form})
