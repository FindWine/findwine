from django.urls import reverse
from rest_framework import serializers

from catalog.serializers import WinePriceSerializer
from wine.context_processors import absolute_url
from wine.models import WineVintage, Wine


class WineSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(source='producer.name', read_only=True)

    class Meta:
        model = Wine
        fields = ('name', 'producer')


class WineVintageSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    avg_rating = serializers.DecimalField(read_only=True, max_digits=3, decimal_places=1)
    available = serializers.BooleanField(read_only=True)
    details_url = serializers.SerializerMethodField()
    wine = WineSerializer(read_only=True)
    preferred_merchant_url = serializers.CharField(source='preferred_merchant.url', read_only=True)
    image_url = serializers.SerializerMethodField()
    sub_category = serializers.CharField(source='sub_category.name')

    class Meta:
        model = WineVintage
        fields = ('url', 'slug', 'wine', 'avg_rating', 'rating_display', 'available',
                  'rating_category', 'details_url', 'category',
                  'sub_category', 'price', 'year', 'preferred_merchant_url', 'image_url')

    def get_details_url(self, obj):
        return reverse('wine:wine_detail_by_slug', args=[obj.slug])

    def get_image_url(self, obj):
        return obj.image_pack_shot.url if obj.image_pack_shot else ''


class MerchantWineVintageSerializer(serializers.ModelSerializer):
    """
    Serializer used to provide details to partners
    """
    price_data = WinePriceSerializer(read_only=True, source='*')
    buy_url = serializers.SerializerMethodField()

    class Meta:
        model = WineVintage
        fields = ('slug', 'long_name', 'price_data', 'buy_url')

    def get_buy_url(self, obj):
        return absolute_url(reverse('clickthrough:buy', args=[obj.slug]))
