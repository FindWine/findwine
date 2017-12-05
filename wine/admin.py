# Register your models here.

from django.contrib import admin
from django.urls import reverse
from .models import Appellation
from .models import Producer
from .models import Wine
from .models import Category
from .models import SubCategory
from .models import Blend
from .models import Winemaker
from .models import WineVintage
from .models import Awardification
from .models import AwardBody
from .models import Award
from .models import WineAward
from .models import Merchant
from .models import Customer
from .models import MerchantWine
from .models import MerchantWineClick
from .models import CustomerWineInterest
from .models import CustomerWineRating
from .models import Grape
from .models import WineGrape
from .models import FoodPairing
from .models import WineFoodPairing


class ProducerAdmin(admin.ModelAdmin):

    def view_on_site(self, obj):
        return reverse('wine:producer_detail_by_slug', kwargs={'slug': obj.slug})


class WineGrapeInline(admin.TabularInline):
    model = WineGrape
    extra = 0


class WineFoodPairingInline(admin.TabularInline):
    model = WineFoodPairing
    extra = 0


class WineAwardInline(admin.TabularInline):
    model = WineAward
    extra = 0


class MerchantWineInline(admin.StackedInline):
    model = MerchantWine
    extra = 0

    
class WineVintageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',        {'fields': ['wine', 'year']}),
        ('Category',    {'fields': ['category', 'sub_category', 'blend', 'appellation', 'winemakers']}),
        ('Attributes',  {'fields': ['sweetness', 'wooded', 'organic', 'contains_sulphites', 'vegetarian']}),
        ('Specs',       {'fields': ['optimal_year_start', 'optimal_year_end', 'temp_min', 'temp_max', 'alcohol_percentage', 'residual_sugar', 'ph', 'total_acidity', 'total_sulphur']}),
        ('Copy',        {'fields': ['notes', 'description']}),
        ('Files',       {'fields': ['image_pack_shot', 'image_label_vertical', 'image_label_horizontal', 'tasting_notes']}),
        ('Status',      {'fields': ['status']}),
    ]
    inlines = [WineGrapeInline, MerchantWineInline, WineAwardInline, WineFoodPairingInline]
    list_display = ('wine', 'year', 'category', 'sub_category', 'status')
    list_filter = ('status', )
    search_fields = ['wine__name', 'wine__producer__name']

    def view_on_site(self, obj):
        return reverse('wine:wine_detail_by_slug', kwargs={'slug': obj.slug})


class WineAdmin(admin.ModelAdmin):
    list_display = ('producer', 'name')

class MerchantWineAdmin(admin.ModelAdmin):
    list_display = ('wine_vintage', 'merchant', 'available')
    list_filter = ('available', 'merchant')


admin.site.register(Appellation)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Blend)
admin.site.register(Winemaker)
admin.site.register(Award)
admin.site.register(Awardification)
admin.site.register(AwardBody)
admin.site.register(WineAward)
admin.site.register(Merchant)
admin.site.register(MerchantWine, MerchantWineAdmin)
admin.site.register(Customer)
admin.site.register(MerchantWineClick)
admin.site.register(CustomerWineInterest)
admin.site.register(CustomerWineRating)
admin.site.register(Grape)
admin.site.register(FoodPairing)
admin.site.register(WineFoodPairing)
admin.site.register(WineGrape)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(WineVintage, WineVintageAdmin)
