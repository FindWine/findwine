# Register your models here.

from django.contrib import admin
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

admin.site.register(Appellation)
admin.site.register(Producer)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Blend)
admin.site.register(Winemaker)
admin.site.register(Award)
admin.site.register(Awardification)
admin.site.register(AwardBody)
admin.site.register(WineAward)
admin.site.register(Merchant)
admin.site.register(MerchantWine)
admin.site.register(Customer)
admin.site.register(MerchantWineClick)
admin.site.register(CustomerWineInterest)
admin.site.register(CustomerWineRating)
admin.site.register(Grape)
admin.site.register(FoodPairing)
admin.site.register(WineFoodPairing)
admin.site.register(WineGrape)


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
        ('Category',    {'fields': ['category', 'sub_category', 'blend', 'appellation', 'winemakers', 'status']}),
        ('Attributes',  {'fields': ['sweetness', 'wooded', 'organic', 'contains_sulphites', 'vegetarian']}),
        ('Specs',       {'fields': ['optimal_year_start', 'optimal_year_end', 'temp_min', 'temp_max', 'alcohol_percentage', 'residual_sugar', 'ph', 'total_acidity', 'total_sulphur']}),
        ('Files',       {'fields': ['image_pack_shot', 'image_label_vertical', 'image_label_horizontal', 'tasting_notes']}),
    ]
    inlines = [WineGrapeInline, MerchantWineInline, WineAwardInline, WineFoodPairingInline]
    list_display = ('wine', 'year', 'category', 'sub_category')
    search_fields = ['wine__short_name', 'wine__producer__name']
    
admin.site.register(WineVintage, WineVintageAdmin)


class WineAdmin(admin.ModelAdmin):
    list_display = ('producer', 'short_name')

admin.site.register(Wine, WineAdmin)
