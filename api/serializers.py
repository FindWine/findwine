from rest_framework import serializers
from wine.models import WineVintage


class WineVintageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineVintage
        # fields = '__all__'
        fields = ('url', 'slug', 'wine', 'category', 'sub_category')
