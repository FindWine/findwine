from django.http import HttpResponseRedirect
from django.urls import reverse


def buy_wine(request, slug):

    return HttpResponseRedirect(reverse('wine:wine_detail_by_slug', kwargs={'slug': slug}))
