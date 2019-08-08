# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def search(request):
    return render(request, 'partners/partner_search.html', {
    })
