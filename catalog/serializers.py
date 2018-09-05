from rest_framework import serializers
from wine.models import WineVintage, Wine, Blend, WineGrape, MerchantWine, WineAward


class BlendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blend
        fields = '__all__'


class WineGrapeSerializer(serializers.ModelSerializer):
    grape = serializers.CharField(source='grape.name', read_only=True)

    class Meta:
        model = WineGrape
        fields = ('grape', 'percentage')


class WineSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(source='producer.name', read_only=True)

    class Meta:
        model = Wine
        fields = ('name', 'producer')


class WineImageSerializer(serializers.ModelSerializer):
    pack_shot = serializers.SerializerMethodField()
    label_vertical = serializers.SerializerMethodField()
    label_horizontal = serializers.SerializerMethodField()

    class Meta:
        model = WineVintage
        fields = ('pack_shot', 'label_vertical', 'label_horizontal')

    def get_pack_shot(self, obj):
        return obj.image_pack_shot.url if obj.image_pack_shot else ''

    def get_label_vertical(self, obj):
        return obj.image_label_vertical.url if obj.image_label_vertical else ''

    def get_label_horizontal(self, obj):
        return obj.image_label_horizontal.url if obj.image_label_horizontal else ''


class MerchantWinePriceSerializer(serializers.ModelSerializer):
    merchant = serializers.CharField(source='merchant.name')

    class Meta:
        model = MerchantWine
        fields = ('merchant', 'price', 'available')


class WinePriceSerializer(serializers.ModelSerializer):
    average_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    listings = MerchantWinePriceSerializer(read_only=True, many=True, source='merchantwine_set')

    class Meta:
        model = WineVintage
        fields = ('average_price', 'listings')


class AwardSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source='award.body.short_name')
    rank = serializers.CharField(source='award.rank')
    year = serializers.IntegerField(source='award.year')

    class Meta:
        model = WineAward
        fields = ('body', 'rank', 'year',)


class WineAwardSerializer(serializers.ModelSerializer):
    average_rating = serializers.CharField(read_only=True, source='rating_display')
    awards = AwardSerializer(read_only=True, many=True, source='wineaward_set')

    class Meta:
        model = WineVintage
        fields = ('average_rating', 'awards')


class WineVintageCatalogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='wine.name')
    producer = serializers.CharField(source='wine.producer.name')
    category = serializers.CharField(source='category.name')
    sub_category = serializers.CharField(source='sub_category.name')
    blend = BlendSerializer(read_only=True)
    winegrape_set = WineGrapeSerializer(read_only=True, many=True)

    images = WineImageSerializer(read_only=True, source='*')
    price_data = WinePriceSerializer(read_only=True, source='*')
    award_data = WineAwardSerializer(read_only=True, source='*')

    class Meta:
        model = WineVintage
        fields = (
            'slug',
            'name',
            'year',
            'producer',
            'category',
            'sub_category',
            'notes',
            'description',
            'sweetness',
            'wooded',
            'organic',
            'contains_sulphites',
            'vegetarian',
            'optimal_year_start',
            'optimal_year_end',
            'temp_min',
            'temp_max',
            'alcohol_percentage',
            'residual_sugar',
            'ph',
            'total_acidity',
            'total_sulphur',
            'tasting_notes',
            'blend',
            'winegrape_set',
            'images',
            'price_data',
            'award_data',
        )
