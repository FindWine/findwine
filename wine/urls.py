from django.conf.urls import url
from django.conf import settings # ADDED FOR MEDIA IN DEV
from django.conf.urls.static import static # ADDED FOR MEDIA IN DEV

from . import views

app_name = 'wine'
urlpatterns = [
    # ex: /
    url(r'^$', views.search, name='search'),
    # ex: /search/
    url(r'^search/$', views.ResultsView.as_view(), name='results'),
    # ex: /ajax/update_subcategories/
    url(r'^ajax/update_subcategories/$', views.update_subcategories, name='update_subcategories'),
    # ex: /index/
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    # ex: /wine/2/  
    url(r'^wine/(?P<pk>[0-9]+)/$', views.WineDetailView.as_view(), name='wine_detail'),
    # ex: /advanced_search/
    url(r'^advanced_search/$', views.AdvancedSearch, name='advanced_search'),
    # ex: /producer/3/  
    url(r'^producer/(?P<pk>[0-9]+)/$', views.ProducerDetailView.as_view(), name='producer_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # NOT SUITABLE FOR PRODCUTION
