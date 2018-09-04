from django.db.models import Min, Avg, Q, Exists, OuterRef
from rest_framework import viewsets
from api.serializers import WineVintageSerializer
from api.util import coerce_to_decimal
from wine.models import WineVintage, MerchantWine, Round


MAX_PRICE = '9999999'

DEFAULT_SORT = ['-avg_rating', 'price']


class WineVintageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WineVintage.objects.all()
    serializer_class = WineVintageSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', 'Red')
        sub_category = self.request.GET.get('sub_category')
        min_price = coerce_to_decimal(self.request.GET.get('min_price', None)) or '0'
        max_price = coerce_to_decimal(self.request.GET.get('max_price', None)) or MAX_PRICE

        sort_by = self.request.GET.get('sort_by', None)

        if sort_by is None:
            sort_by = DEFAULT_SORT
        elif sort_by == '-avg_rating':
            # add second layer of sorting
            sort_by = DEFAULT_SORT
        else:
            sort_by = sort_by.split(',')
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
        ).select_related('wine_vintage', 'wine_vintage__sub_category')

        # 6 Restrict MerchantWines to the selected sub_category or leave if no sub_category is selected
        if sub_category:
            results_list = results_list.filter(wine_vintage__sub_category__name__in=sub_category.split(','))

        # 7 Restrict MerchantWines to lowest price version(s) of same wine_vintage
        wines = WineVintage.objects.distinct().filter(merchantwine__in=results_list)
        # 8 Only show lowest price and add average rating
        wines = _add_computed_columns(wines)
        wines = wines.order_by(*sort_by)
        # todo: if necessary
        # #9 Restrict MerchantWines to lowest minimum_purchase_unit of same wine_vintage, price and merchant
        # # NOT WORKING min_units = results_list.values('wine_vintage').annotate(smallest_unit=Min('minimum_purchase_unit'))
        # # NOT WORKING results_list = results_list.filter(minimum_purchase_unit__in=min_units.values('smallest_unit'))
        return wines


class WineVintageSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WineVintage.objects.all()
    serializer_class = WineVintageSerializer

    def get_queryset(self):
        query_text = self.request.GET.get('q', '')
        wines = WineVintage.objects.exclude(
            merchantwine__isnull=True,
        ).exclude(
            wineaward__isnull=True
        )
        for term in query_text.split():
             query = Q(wine__name__icontains=term) | Q(wine__producer__name__icontains=term)
             wines = wines.filter(query)
        wines = _add_computed_columns(wines)
        return wines.order_by('-available', *DEFAULT_SORT)


def _add_computed_columns(wines):
    return wines.annotate(
        available=Exists(MerchantWine.objects.filter(available=True, wine_vintage=OuterRef('pk'))),
        price=Round(Min('merchantwine__price')),
        avg_rating=Round(Avg('wineaward__award__tier__normalised_rating')),

    )
