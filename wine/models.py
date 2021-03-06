# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from urllib import parse
from django.core.exceptions import ValidationError

from django.db import models
from django.db.models import Avg
from geoposition.fields import GeopositionField
from jsonfield import JSONField
from wine.const import get_all_country_wine_choices, get_all_merchant_country_choices, \
    get_all_currency_choices, SOUTH_AFRICA_CODE, SOUTH_AFRICAN_RAND_CODE
from wine.geoposition import geoposition_to_dms_string
from wine.util import generate_unique_slug, MAX_UNIQUE_CHARFIELD, generate_unique_producer_slug
from django.db.models import Func


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


class Country(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=2, help_text="2 digit ISO e.g. ZA for South Africa")
    currency_name = models.CharField(max_length=256, null=True, blank=True)
    currency_code = models.CharField(max_length=3, help_text="3 digit ISO e.g. ZAR for South Africa")
    currency_symbol = models.CharField(null=True, blank=True, max_length=3)
    is_producer = models.NullBooleanField(help_text="No for a country that should not show up in Wine Vintage choices")
    is_merchant = models.NullBooleanField(help_text="Yes to add a country that should show up in Merchant choices")

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(
            code='ZA', defaults={'name': 'South Africa', 'currency_code': 'ZAR'}
        )[0].pk

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Appellation(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(choices=get_all_country_wine_choices(), max_length=2, default=SOUTH_AFRICA_CODE)
    level1 = models.CharField(null=True, blank=True, max_length=256)
    level2 = models.CharField(null=True, blank=True, max_length=256)
    level3 = models.CharField(null=True, blank=True, max_length=256)
    level4 = models.CharField(null=True, blank=True, max_length=256)
    level5 = models.CharField(null=True, blank=True, max_length=256)
    type = models.CharField(null=True, blank=True, max_length=256)
    country_model = models.ForeignKey("Country", null=True, blank=True)    

    def __str__(self):
        return self.name + ', ' + self.country

    class Meta:
        ordering = ['name']


class Producer(models.Model):
    slug = models.CharField(max_length=MAX_UNIQUE_CHARFIELD, unique=True, editable=False)
    name = models.CharField(max_length=256)
    country = models.CharField(choices=get_all_country_wine_choices(), max_length=2, default=SOUTH_AFRICA_CODE)
    country_model = models.ForeignKey("Country", null=True, blank=True)
    appellation_primary = models.ForeignKey("Appellation", null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=256)
    coordinates_google = GeopositionField(null=True, blank=True)
    google_place_id = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_mon = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_tue = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_wed = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_thu = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_fri = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_sat = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_sun = models.CharField(null=True, blank=True, max_length=256)
    opening_hours_holidays = models.CharField(null=True, blank=True, max_length=256)
    closed_days = models.CharField(null=True, blank=True, max_length=256)
    telephone_tasting = models.CharField(null=True, blank=True, max_length=64)
    email_tasting = models.EmailField(max_length=254, null=True, blank=True)
    url = models.URLField(null=True, blank=True, max_length=256)
    facebook = models.URLField(null=True, blank=True, max_length=256)
    twitter = models.URLField(null=True, blank=True, max_length=256)
    instagram = models.URLField(null=True, blank=True, max_length=256)
    linkedin = models.URLField(null=True, blank=True, max_length=256)
    tasting_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    tasting_currency = models.CharField(null=True, blank=True, choices=get_all_currency_choices(), max_length=3)
    logo = models.ImageField(upload_to='images/producer_logos/', null=True, blank=True, max_length=500)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/producer_images/', null=True, blank=True, max_length=500)

    @property
    def coordinates_display(self):
        if self.coordinates_google:
            return geoposition_to_dms_string(self.coordinates_google)
        else:
            return self.coordinates_text

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_producer_slug(self)
        super(Producer, self).save(*args, **kwargs)

    def get_top_wines(self):
        return WineVintage.with_rating().filter(
            wine__producer=self, merchantwine__available=True
        ).order_by('-avg_rating')


class Range(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(blank=True, default="", max_length=100)
    producer = models.ForeignKey("Producer")
    name = models.CharField(max_length=MAX_UNIQUE_CHARFIELD)
    
    def __str__(self):
        return self.producer.name + ' ' + self.name

    class Meta:
        ordering = ['producer', 'name']
        unique_together = (("producer", "name"),)

class Wine(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(blank=True, default="", max_length=100)
    producer = models.ForeignKey("Producer")
    range = models.ForeignKey("Range", null=True, blank=True)
    name = models.CharField(max_length=256)
    wine_range = models.CharField(null=True, blank=True, max_length=256)
    image_pack_shot = models.ImageField(upload_to='images/wine_packshots/', null=True, blank=True,
                                        max_length=500)
    image_label_vertical = models.ImageField(upload_to='images/wine_label_vertical/', null=True, blank=True,
                                             max_length=500)
    fact_sheet = models.FileField(upload_to='documents/wine_fact_sheets/', null=True, blank=True, max_length=500)

    def __str__(self):
        return self.producer.name + ' ' + self.name

    class Meta:
        ordering = ['producer', 'name']
        unique_together = (("producer", "name"),)


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Blend(models.Model):
    category = models.ForeignKey("Category")
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Winemaker(models.Model):
    forename_1 = models.CharField(max_length=256)
    forename_2 = models.CharField(null=True, blank=True, max_length=256)
    surname = models.CharField(max_length=256)
    facebook = models.URLField(null=True, blank=True, max_length=256)
    twitter = models.URLField(null=True, blank=True, max_length=256)
    instagram = models.URLField(null=True, blank=True, max_length=256)
    linkedin = models.URLField(null=True, blank=True, max_length=256)

    def __str__(self):
        return '{} {} {}'.format(self.forename_1, '' if not self.forename_2 else ' {}'.format(self.forename_2), self.surname)

    class Meta:
        ordering = ['surname', 'forename_1', 'forename_2']


class Viticulturist(models.Model):
    forename_1 = models.CharField(max_length=256)
    forename_2 = models.CharField(null=True, blank=True, max_length=256)
    surname = models.CharField(max_length=256)
    facebook = models.URLField(null=True, blank=True, max_length=256)
    twitter = models.URLField(null=True, blank=True, max_length=256)
    instagram = models.URLField(null=True, blank=True, max_length=256)
    linkedin = models.URLField(null=True, blank=True, max_length=256)

    def __str__(self):
        return '{} {} {}'.format(self.forename_1, '' if not self.forename_2 else ' {}'.format(self.forename_2), self.surname)

    class Meta:
        ordering = ['surname', 'forename_1', 'forename_2']
        

class WineVintage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(blank=True, default="", max_length=100)
    slug = models.CharField(max_length=MAX_UNIQUE_CHARFIELD, unique=True, editable=False)
    wine = models.ForeignKey("Wine")
    category = models.ForeignKey("Category")
    sub_category = models.ForeignKey("SubCategory")
    blend = models.ForeignKey("Blend", null=True, blank=True)
    appellation = models.ForeignKey("Appellation", null=True, blank=True)
    winemakers = models.ManyToManyField("Winemaker", blank=True, related_name='winemakers')
    viticulturists = models.ManyToManyField("Viticulturist", blank=True, related_name='viticulturists')
    vintage_type = models.CharField(
        choices=(
            ('Vintage', "Vintage"),
            ('NV', "NV"),
        ),
        max_length=20, default='Vintage'
    )
    year = models.PositiveIntegerField(help_text="This is the vintage i.e. when harvest took place")
    release_year = models.PositiveIntegerField(null=True, blank=True, help_text="When the wine was released")
    notes = models.TextField(blank=True)
    description = models.TextField(blank=True)
    sweetness = models.CharField(
        choices=(
            ('Bone Dry', "Bone Dry"),
            ('Dry', "Dry"),
            ('Semi-Sweet', "Semi-Sweet"),
            ('Sweet', "Sweet"),
            ('Very Sweet', "Very Sweet"),
        ),
        max_length=20, null=True, blank=True
    )
    wooded = models.NullBooleanField()
    organic = models.NullBooleanField()
    biodynamic = models.NullBooleanField()
    contains_sulphites = models.NullBooleanField()
    vegetarian = models.NullBooleanField()
    vegan = models.NullBooleanField()
    optimal_year_start = models.PositiveIntegerField(null=True, blank=True)
    optimal_year_end = models.PositiveIntegerField(null=True, blank=True)
    temp_min = models.PositiveIntegerField(null=True, blank=True)
    temp_max = models.PositiveIntegerField(null=True, blank=True)
    alcohol_percentage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    residual_sugar = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    ph = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    volatile_acidity = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    total_acidity = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    total_sulphur = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    image_pack_shot = models.ImageField(upload_to='images/winevintage_packshots/', null=True, blank=True,
                                        max_length=500)
    image_label_vertical = models.ImageField(upload_to='images/winevintage_label_vertical/', null=True, blank=True,
                                             max_length=500)
    tasting_notes = models.FileField(upload_to='documents/tasting_notes/', null=True, blank=True, max_length=500)
    status = models.CharField(
        choices=(
            ('Incomplete_Unavailable', "Incomplete and Unavailable"),
            ('Incomplete_Available', "Incomplete but Available"),
            ('Complete_Unavailable', "Complete but Unavailable"),
            ('Complete_Available', "Complete and Available"),
            ('Approved', "Approved"),
        ),
        max_length=30, default='Incomplete_Unavailable'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super(WineVintage, self).save(*args, **kwargs)

    def clean(self):
        if self.sub_category_id is not None:
            if not self.sub_category.category.filter(id=self.category.id).exists():
                raise ValidationError('Category {} and SubCategory {} are not a valid combination!'.format(
                    self.category, self.sub_category
                ))

    @classmethod
    def with_rating(cls):
        return cls.objects.annotate(
            avg_rating=Round(Avg('wineaward__award__tier__normalised_rating')),
        )

    @property
    def preferred_merchant(self):
        """
        Tiebreaking Rules (in order):
         - Choose the cheapest
         - Choose the lowest merchant priority
         - Choose by ID (arbitrary)
        """
        qs = self.merchantwine_set.order_by('price', 'merchant__priority', 'pk')
        if qs.exists():
            return qs[0]

    @property
    def long_name(self):
        """Returns the wine's full name including producer and year."""
        return '%s %s' % (self.wine, self.year)

    @property
    def rating(self):
        """Aggregate normalised rating from the wine awards."""
        return WineAward.objects.filter(wine_vintage=self).aggregate(
            avg_rating=Avg('award__tier__normalised_rating'))

    def get_price(self):
        prices = self.merchantwine_set.filter(available=True).order_by('price').values_list('price', flat=True)
        return prices[0] if prices else None

    @property
    def average_price(self):
        return self.merchantwine_set.aggregate(
            average_price=Avg('price')
        ).get('average_price', None)

    @property
    def rating_display(self):
        """Aggregate normalised rating from the wine awards."""
        rating = self.rating
        if rating and rating['avg_rating']:
            rating = rating['avg_rating']
            display = '{0:.1f}'.format(rating)
            # hack - manually show perfect 10s
            if display == '10.0':
                display = '10'
            return display
        else:
            return '?'

    @property
    def rating_category(self):
        """Aggregate normalised rating from the wine awards."""
        rating = self.rating
        if rating and rating['avg_rating']:
            if rating['avg_rating'] >= 9:
                return 'gold'
            elif rating['avg_rating'] >= 8:
                return 'sliver'
            else:
                return 'bronze'

    @property
    def other_vintages(self):
        return WineVintage.objects.filter(wine=self.wine).exclude(id=self.id).filter(
            merchantwine__available=True
        ).distinct()

    def get_prioritized_purchase_options(self):
        return self.merchantwine_set.filter(available=True).select_related('merchant').order_by(
            'price', 'minimum_purchase_unit', 'merchant__priority'
        )

    def __str__(self):
        return self.long_name

    class Meta:
        ordering = ['wine', 'year']
        unique_together = (("wine", "year"),)


class Awardification(models.Model):
    tier = models.CharField(choices=(
    ('1', "1/100/Decanter Best in Show/IWC Trophy/Platters Wine of year"),
    ('2', "2/98-99/Decanter Platinum/IWC Gold/Platters 5*/IWSC Trophy"),
    ('3', "3/95-97/Decanter Gold/IWC Silver/IWSC Gold Outstanding"),
    ('4', "4/90-94/Decanter Silver/IWC Bronze/Platters 4.5*/IWSC Gold/Veritas Double Gold"),
    ('5', "5/86-89/Decanter Bronze/IWC Commended/Platter's 4*/IWSC Silver Outstanding/Veritas Gold"),
    ('6', "6/83-85/Decanter Seal of approval/Platter's 3.5*/IWSC Silver/Veritas Silver"),
    ('7', "7/80-82/Platter's 3*"),
    ('8', "8/76-79/Platter's 2.5*/IWSC Bronze/Veritas Bronze"),
    ('9', "9/73-75/Platter's 2*"),
    ('10', "10/70-72"),
    ('11', "11/50-69"),
    ),
    max_length=2
    )
    conversion = models.CharField(null=True, blank=True, max_length=256)
    normalised_rating = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g. 10.00")

    def __str__(self):
        return 'Tier ' + str(self.tier) + ': ' + str(self.normalised_rating)

    class Meta:
        ordering = ['tier']


class AwardBody(models.Model):
    short_name = models.CharField(max_length=256)
    long_name = models.CharField(null=True, blank=True, max_length=256)
    url = models.URLField(null=True, blank=True, max_length=256)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering = ['short_name']


class Award(models.Model):
    body = models.ForeignKey("AwardBody")
    tier = models.ForeignKey("Awardification")
    rank = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/award_images/', null=True, blank=True, max_length=500)
    recognition_url = models.URLField(null=True, blank=True, max_length=256)

    @property
    def full_name(self):
        "Returns the award's full name."
        return '%s %s %s' % (self.body, self.rank, self.year)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['body', 'year', 'tier']


class WineAward(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    award = models.ForeignKey("Award")
    recognition_url = models.URLField(null=True, blank=True, max_length=256)

    @property
    def normalised_rating(self):
        "Get the normalised rating from the award."
        return self.award.tier.normalised_rating

    def __str__(self):
        return str(self.wine_vintage) + ' -> ' + str(self.award)

    class Meta:
        ordering = ['wine_vintage', 'award']


class Merchant(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(choices=get_all_merchant_country_choices(), max_length=2, default=SOUTH_AFRICA_CODE)
    country_model = models.ForeignKey("Country", null=True, blank=True)
    is_active = models.NullBooleanField(help_text="Yes to add a merchant that should show up in MerchantWine choices")
    priority = models.PositiveIntegerField()
    sales_commission_percentage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2,
                                                      help_text="Full percentage e.g. 8 for 8%")
    cost_per_click = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    currency = models.CharField(choices=get_all_currency_choices(), max_length=3, default=SOUTH_AFRICAN_RAND_CODE)
    merchant_type = models.CharField(
        choices=(
            ('1', "CPS or Commission on sale"),
            ('2', "CPC or Cost Per Click"),
            ('3', "Combo or CPS and CPC"),
        ),
        max_length=2
    )
    delivery_fee = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    delivery_fees = models.TextField(null=True, blank=True)
    delivery_threshold = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    logo = models.ImageField(upload_to='images/merchant_logos/', null=True, blank=True, max_length=500)
    url = models.URLField(null=True, blank=True, max_length=256)
    affiliate_params = JSONField(default={}, blank=True)

    def __str__(self):
        return self.name + ' ' + self.country

    class Meta:
        ordering = ['name', 'country']


class Customer(models.Model):
    forename_1 = models.CharField(max_length=256)
    forename_2 = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    email = models.EmailField(max_length=254, null=True, blank=True)

    telephone_cell = models.CharField(null=True, blank=True, max_length=64)
    country = models.CharField(max_length=2, help_text="2 digit ISO e.g. ZA for South Africa", default=SOUTH_AFRICA_CODE)
    state = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    post_code = models.CharField(max_length=16)
    address_line_1 = models.CharField(max_length=256)
    address_line_2 = models.CharField(max_length=256)
    newsletter_consent = models.NullBooleanField()

    def __str__(self):
        return str(self.surname) + ', ' + str(self.forename_1) + ' ' + str(self.forename_2)

    class Meta:
        ordering = ['surname', 'forename_1', 'forename_2']


class MerchantWine(models.Model):
    merchant = models.ForeignKey("Merchant")
    wine_vintage = models.ForeignKey("WineVintage")
    # Add Country table in place and use currency from that
    country_model = models.ForeignKey("Country", default=Country.get_default, null=True, blank=True)
    country = models.CharField(choices=get_all_merchant_country_choices(), max_length=2, default=SOUTH_AFRICA_CODE)
    currency = models.CharField(choices=get_all_currency_choices(), max_length=3, default=SOUTH_AFRICAN_RAND_CODE)
    price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2, help_text="e.g. 150.00")
    url = models.URLField(max_length=256)
    external_id = models.CharField(null=True, blank=True, max_length=256)
    available = models.NullBooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(blank=True, default="", max_length=100)
    purchase_unit = models.CharField(choices=(
        ('750', "Bottle 750ml"),
        ('187', "Split 187ml"),
        ('375', "Half-Bottle 375ml"),
        ('500', "Bottle 500ml"),
        ('1000', "Growler 1 litre"),
        ('1500', "Magnum 1.5 litres"),
        ('3000', "Jeroboam or Double Magnum 3 litres"),
        ('4500', "Rehoboam 4.5 litres"),
        ('5000', "5 litres"),
        ('6000', "Imperial or Methuselah 6 litres"),
        ('9000', "Salmanazar 9 litres"),
        ('12000', "Balthazar 12 litres"),
        ('15000', "Nebuchadnezzar 15 litres"),
    ),
        max_length=5
    )
    minimum_purchase_unit = models.PositiveIntegerField()

    @property
    def rounded_price(self):
        return int(self.price) if self.price is not None else ''

    def get_url(self, additional_params=None):
        """
        Constructs a URL, incorporating any affiliate logic, if necessary
        """
        params = {}
        if additional_params:
            params.update(additional_params)
        if self.merchant.affiliate_params:
            params.update(self.merchant.affiliate_params)
        if params:
            # sort for tests
            sorted_params = OrderedDict()
            for key in sorted(params.keys()):
                sorted_params[key] = params[key]
            sep = '?' if '?' not in self.url else '&'
            return '{}{}{}'.format(self.url, sep, parse.urlencode(sorted_params))
        else:
            return self.url

    def __str__(self):
        return str(self.wine_vintage) + ' - ' + str(self.merchant)

    class Meta:
        ordering = ['wine_vintage', 'merchant']


class MerchantWineClick(models.Model):
    merchant_wine = models.ForeignKey("MerchantWine")
    customer = models.ForeignKey("Customer")
    clicked_timestamp = models.DateTimeField(auto_now=False)
    fulfilled_timestamp = models.DateTimeField(null=True, blank=True, auto_now=False)
    currency = models.CharField(null=True, blank=True, max_length=3, default=SOUTH_AFRICAN_RAND_CODE)
    price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)


class CustomerWineInterest(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    customer = models.ForeignKey("Customer")
    interest_type = models.CharField(choices=(
    ('1', "Notify when wine becomes available"),
    ),
                                     max_length=2
    )
    active_status = models.NullBooleanField()

    def __str__(self):
        return str(self.customer) + ' -> ' + str(self.wine_vintage)

    class Meta:
        ordering = ['customer', 'wine_vintage']


class CustomerWineRating(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    customer = models.ForeignKey("Customer")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer) + ' -> ' + str(self.wine_vintage)

    class Meta:
        ordering = ['customer', 'wine_vintage']


class Grape(models.Model):
    name = models.CharField(max_length=128)
    alternate_names = models.CharField(blank=True, max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WineGrape(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    grape = models.ForeignKey("Grape")
    percentage = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2,
                                     help_text="Percentage value eg. '69.0' for 69%")

    def __str__(self):
        return str(self.wine_vintage) + ' -> ' + str(self.grape)

    class Meta:
        ordering = ['-percentage']


class FoodPairing(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(choices=(
    ('Meat', "Meat"),
    ('Poultry', "Poultry"),
    ('Seafood', "Seafood"),
    ('Dairy', "Dairy"),
    ('Vegetable', "Vegetable"),
    ('Herb or Spice', "Herb or Spice"),
    ('Starch', "Starch"),
    ('Sweet', "Sweet"),
    ),
                                max_length=64
    )

    def __str__(self):
        return self.category + ': ' + self.name

    class Meta:
        ordering = ['category', 'name']


class WineFoodPairing(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    food_pairing = models.ForeignKey("FoodPairing")
    strength = models.CharField(choices=(
    ('1', "Perfect"),
    ('2', "Ok"),
    ),
                                max_length=2, blank=True, default='2'
    )

    def __str__(self):
        return str(self.wine_vintage) + ' -> ' + str(self.food_pairing)

    class Meta:
        ordering = ['wine_vintage', 'food_pairing']


class Critic(models.Model):
    forename_1 = models.CharField(max_length=256)
    forename_2 = models.CharField(null=True, blank=True, max_length=256)
    surname = models.CharField(max_length=256)
    initials = models.CharField(max_length=3)
    url = models.URLField(null=True, blank=True, max_length=256)

    def __str__(self):
        return '{} {} {}'.format(self.forename_1, '' if not self.forename_2 else ' {}'.format(self.forename_2), self.surname)

    class Meta:
        ordering = ['surname', 'forename_1', 'forename_2']


class CriticReport(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(blank=True, default="", max_length=100)
    critic = models.ForeignKey("Critic")
    name = models.CharField(max_length=MAX_UNIQUE_CHARFIELD, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.critic.name + ' ' + self.name + ' ' + self.year

    class Meta:
        ordering = ['critic', 'name', 'year']
        unique_together = (("critic", "name", "year"),)


class CriticReview(models.Model):
    wine_vintage = models.ForeignKey("WineVintage")
    critic = models.ForeignKey("Critic")
    score = models.CharField(max_length=4)
    score_max = models.CharField(max_length=4, default="100")
    review = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    month = models.PositiveIntegerField(null=True, blank=True)
    recognition_url = models.URLField(null=True, blank=True, max_length=256)

    def __str__(self):
        return str(self.critic) + ' -> ' + str(self.score)

    class Meta:
        ordering = ['wine_vintage', 'critic']
