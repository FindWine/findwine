from django.db.models import Min, Avg
from rest_framework import viewsets
from api.serializers import WineVintageSerializer
from wine.models import WineVintage, MerchantWine
from wine.views import Round


MAX_PRICE = 9999999


class WineVintageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WineVintage.objects.all()
    serializer_class = WineVintageSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', 'Red')
        sub_category = self.request.GET.get('sub_category')
        min_price = self.request.GET.get('min_price', 0)
        max_price = self.request.GET.get('max_price', MAX_PRICE)
        sort_by = self.request.GET.get('sort_by', None)
        if sort_by is None:
            sort_by = ['-avg_rating', 'price']
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
        wines = wines.annotate(
            price=Round(Min('merchantwine__price')),
            avg_rating=Round(Avg('wineaward__award__tier__normalised_rating')),

        )
        wines = wines.order_by(*sort_by)
        # todo: if necessary
        # #9 Restrict MerchantWines to lowest minimum_purchase_unit of same wine_vintage, price and merchant
        # # NOT WORKING min_units = results_list.values('wine_vintage').annotate(smallest_unit=Min('minimum_purchase_unit'))
        # # NOT WORKING results_list = results_list.filter(minimum_purchase_unit__in=min_units.values('smallest_unit'))
        return wines
