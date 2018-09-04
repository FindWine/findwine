# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_GET
from rest_framework import viewsets

from catalog.serializers import WineVintageCatalogSerializer
from wine.context_processors import absolute_url
from wine.models import WineVintage, Producer
from integrations.tasks import fail_task


class WineVintageCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WineVintage.objects.all()
    serializer_class = WineVintageCatalogSerializer
    lookup_field = 'slug'


class WineDetailCatalogView(generic.DetailView):
    model = WineVintage
    template_name = 'catalog/wine_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WineDetailCatalogView, self).get_context_data(**kwargs)
        # social/meta stuff
        context['page_title'] = self.object.long_name
        context['page_description'] = 'Find the best place to buy {}'.format(self.object.long_name)
        if self.object.image_pack_shot:
            context['page_image'] = self.object.image_pack_shot.url
        return context


class ProducerDetailView(generic.DetailView):
    model = Producer
    template_name = 'wine/producer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProducerDetailView, self).get_context_data(**kwargs)
        # social/meta stuff
        context['page_title'] = self.object.name
        context['page_description'] = 'Find great wine from {}'.format(self.object.name)
        if self.object.logo:
            context['page_image'] = self.object.logo.url
        return context


@require_GET
def error(request):
    raise Exception('Simulated Failure!')


@require_GET
def celery_error(request):
    fail_task.delay()
    return HttpResponse('Triggered a celery task that should fail.')


@require_GET
def sitemap(request):
    lines = []
    for producer in Producer.objects.all():
        lines.append(absolute_url(reverse('wine:producer_detail_by_slug', args=[producer.slug])))
    for wine_vintage in WineVintage.objects.all():
        lines.append(absolute_url(reverse('wine:wine_detail_by_slug', args=[wine_vintage.slug])))
    return HttpResponse('\n'.join(lines), content_type='text/plain')
