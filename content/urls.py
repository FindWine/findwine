from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'content'
urlpatterns = [
    # ex: /
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^terms/$', views.TermsView.as_view(), name='terms'),
    url(r'^partners/$', views.PartnersView.as_view(), name='terms'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # TODO: NOT SUITABLE FOR PRODCUTION
