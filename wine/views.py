# -*- coding: utf-8 -*-

from django.db.models import Avg, Min, Func
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from .models import WineVintage, MerchantWine, Producer, SubCategory
from .forms import BasicSearchForm, AdvancedSearchForm


class IndexView(generic.ListView):
    template_name = 'wine/index.html'
    context_object_name = 'winevintage_list'

    def get_queryset(self):
        """Return the first 500 wine vintages ordered by name."""
        return WineVintage.objects.all()[:500]


def search(request):
    # REMOVE POST STUFF? ADD???
    if request.method == 'POST':
        form = BasicSearchForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data[
                'sub_category']  #SubCategory.objects.filter(category__name__exact=category)
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            # redirect to a new URL:
            return render(request, 'wine/search.html', {'form': form})
    else:
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
        #1 Add country
        #2 Restrict MerchantWines to those that are available
        results_list = MerchantWine.objects.filter(available__exact="True")
        #3 Restrict MerchantWines to those that are above or equal to the minimum price
        results_list = results_list.filter(price__gte=min_price)
        #4 Restrict MerchantWines to those that are below or equal to the maximum price
        results_list = results_list.filter(price__lte=max_price)
        #5 Restrict MerchantWines to the selected category
        results_list = results_list.filter(wine_vintage__category__name__exact=category)
        #6 Restrict MerchantWines to the selected sub_category or leave if no sub_category is selected NB! UPDATE FOR MULTIPLE SELECT
        if sub_category != 'All':
            results_list = results_list.filter(wine_vintage__sub_category__name__exact=sub_category)
        else:
            results_list = results_list
        #7 Restrict MerchantWines to lowest price version(s) of same wine_vintage
        minimum_prices = results_list.values('wine_vintage').annotate(lowest_price=Min('price'))
        results_list = results_list.filter(price__in=minimum_prices.values('lowest_price'))
        #8 Restrict MerchantWines to preferred merchant of same wine_vintage and price
        preferred_merchants = results_list.values('wine_vintage').annotate(
            lowest_priority=Min('merchant__priority'))
        results_list = results_list.filter(merchant__priority__in=preferred_merchants.values('lowest_priority'))
        #9 Restrict MerchantWines to lowest minimum_purchase_unit of same wine_vintage, price and merchant
        # NOT WORKING min_units = results_list.values('wine_vintage').annotate(smallest_unit=Min('minimum_purchase_unit'))
        # NOT WORKING results_list = results_list.filter(minimum_purchase_unit__in=min_units.values('smallest_unit'))
        #10 Remove duplicates
        # TO DO
        #11 Add the rating to each MerchantWine
        results_list = results_list.annotate(
            rating=Round(Avg('wine_vintage__wineaward__award__tier__normalised_rating')))
        #12 Order by rating and then price
        orders = ['-rating', 'price']
        results_list = results_list.order_by(*orders)
        return results_list


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
