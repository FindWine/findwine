from rest_framework import routers

# Serializers define the API representation.
from api.views import WineVintageViewSet, WineVintageSearchViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'wine-vintages', WineVintageViewSet)
router.register(r'search', WineVintageSearchViewSet)
