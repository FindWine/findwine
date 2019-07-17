# Register your models here.

from django.contrib import admin
from django.urls import reverse
from .models import Country
from .models import Appellation
from .models import Producer
from .models import Range
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


class ModelSaveRecordingMixIn(object):

    def save_model(self, request, obj, form, change):
        # hat tip: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
        obj.last_modified_by = request.user.username
        super(ModelSaveRecordingMixIn, self).save_model(request, obj, form, change)


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
    readonly_fields = ['last_modified_by']


class WineVintageAdmin(ModelSaveRecordingMixIn, admin.ModelAdmin):
    fieldsets = [
        ('Name',        {'fields': ['wine', 'vintage_type', 'year', 'release_year', 'last_modified_by']}),
        ('Category',    {'fields': ['category', 'sub_category', 'blend', 'appellation', 'winemakers']}),
        ('Attributes',  {'fields': ['sweetness', 'wooded', 'organic', 'contains_sulphites', 'vegetarian']}),
        ('Specs',       {'fields': ['optimal_year_start', 'optimal_year_end', 'temp_min', 'temp_max', 'alcohol_percentage', 'residual_sugar', 'ph', 'total_acidity', 'total_sulphur']}),
        ('Copy',        {'fields': ['notes', 'description']}),
        ('Files',       {'fields': ['image_pack_shot', 'image_label_vertical', 'tasting_notes']}),
        ('Status',      {'fields': ['status']}),
    ]
    inlines = [WineGrapeInline, MerchantWineInline, WineAwardInline, WineFoodPairingInline]
    list_display = ('wine', 'year', 'category', 'sub_category', 'status', 'last_modified')
    list_filter = ('status', 'date_created', 'last_modified')
    search_fields = ['wine__name', 'wine__producer__name', 'year']
    readonly_fields = ['last_modified_by']

    def save_formset(self, request, form, formset, change):
        # hat tip: https://stackoverflow.com/a/1477428/8207
        if formset.model == MerchantWine:
            # updating formset
            instances = formset.save(commit=False)
            for instance in instances:
                instance.last_modified_by = request.user.username
                instance.save()
            formset.save_m2m()
            return instances
        else:
            return formset.save()

    def view_on_site(self, obj):
        return reverse('wine:wine_detail_by_slug', kwargs={'slug': obj.slug})


class WineAdmin(ModelSaveRecordingMixIn, admin.ModelAdmin):
    list_display = ('producer', 'name', 'last_modified')
    list_filter = ('date_created', 'last_modified')
    search_fields = ('producer__name', 'name')
    readonly_fields = ['last_modified_by']


class ProducerAdmin(ModelSaveRecordingMixIn, admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('country',)
    search_fields = ('name',)

    
class RangeAdmin(ModelSaveRecordingMixIn, admin.ModelAdmin):
    list_display = ('name', 'producer')
    readonly_fields = ['last_modified_by']
    search_fields = ('producer__name', 'name')
    
    
class MerchantWineAdmin(ModelSaveRecordingMixIn, admin.ModelAdmin):
    list_display = ('wine_vintage', 'merchant', 'available', 'last_modified')
    list_filter = ('available', 'merchant', 'last_modified')
    search_fields = ('wine_vintage__wine__name', 'wine_vintage__wine__producer__name', 'wine_vintage__year', 'external_id')
    readonly_fields = ['last_modified_by']


admin.site.register(Country)
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
admin.site.register(Range, RangeAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(WineVintage, WineVintageAdmin)
