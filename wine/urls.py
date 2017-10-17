from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views
from rest_framework import routers


app_name = 'wine'
urlpatterns = [
    # ex: /
    url(r'^$', views.search, name='search'),
    # ex: /search/
    url(r'^search/$', views.ResultsView.as_view(), name='results'),
    # ex: /index/
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    # ex: /wine/paul-cluver-noble-late-harvest-2014/
    url(r'^wine/(?P<slug>[A-Za-z0-9_-]+)/$', views.WineDetailView.as_view(), name='wine_detail_by_slug'),
    # ex: /advanced_search/
    url(r'^advanced_search/$', views.AdvancedSearch, name='advanced_search'),
    # ex: /producer/3/
    url(r'^producer/(?P<pk>[0-9]+)/$', views.ProducerDetailView.as_view(), name='producer_detail'),
    url(r'^500/$', views.error, name='simulate_error'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOT SUITABLE FOR PRODCUTION
