from django.urls import reverse
from rest_framework import serializers
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
