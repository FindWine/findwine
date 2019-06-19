from django.conf.urls import url

from . import views

app_name = 'clickthrough'
urlpatterns = [
    url(r'^buy-wine/(?P<slug>[A-Za-z0-9_-]+)/$', views.buy_wine, name='buy'),
]
