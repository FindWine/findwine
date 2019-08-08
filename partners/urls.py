from django.conf.urls import url

from . import views


app_name = 'partners'
urlpatterns = [
    url(r'^search/$', views.search, name='partner_search'),
]
