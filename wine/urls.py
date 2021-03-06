from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'wine'
urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^search/$', views.search, name='search_explicit'),
    url(r'^search-by-name/$', views.search_by_name, name='search_by_name'),
    # ex: /wine/paul-cluver-noble-late-harvest-2014/
    url(r'^wine/(?P<slug>[A-Za-z0-9_-]+)/$', views.WineDetailView.as_view(), name='wine_detail_by_slug'),
    # ex: /producer/warwick/
    url(r'^producer/(?P<slug>[A-Za-z0-9_-]+)/$', views.ProducerDetailView.as_view(),
        name='producer_detail_by_slug'),
    url(r'^price-widget-test/$', views.price_widget_test, name='price_widget_test'),
    url(r'^500/$', views.error, name='simulate_error'),
    url(r'^celery_500/$', views.celery_error, name='simulate_celery_error'),
    url(r'^sitemap.txt$', views.sitemap, name='sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # NOT SUITABLE FOR PRODCUTION
