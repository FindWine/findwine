from django.conf.urls import url


from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/wines', views.WineVintageCatalogViewSet)

urlpatterns = [
    url(r'^wine/(?P<slug>[A-Za-z0-9_-]+)/$', views.WineDetailCatalogView.as_view(), name='wine_detail_by_slug'),
] + router.urls
