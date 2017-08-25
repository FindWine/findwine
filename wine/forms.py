# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import WineVintage, Category, SubCategory, MerchantWine

class BasicSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        to_field_name="name",
        empty_label=None,
        initial="Red")
    # dynamic selection is handled by javascript so no need to base this off a model/queryset
    sub_category = forms.ChoiceField(
        required=False,
        label='Type',
        widget=forms.Select) # forms.SelectMultiple or forms.CheckboxSelectMultiple for multiple
    # How to have an all option? How to limit depending on category?
    min_price = forms.IntegerField(label='Minimum Price', min_value=0, initial=0)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, initial=500)
    # Max what for slider? max_value=Max(merchantwine__price)+100
    # country = hidden from autodefined country = forms.CharField(widget=forms.HiddenInput())


class AdvancedSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        to_field_name="name",
        empty_label=None,
        initial="Red")
    sub_category = forms.ModelMultipleChoiceField(
        required=False,
        label='Type',
        queryset= SubCategory.objects.filter(category__name__exact="Red"),
        to_field_name="name",
        widget=forms.Select) # forms.SelectMultiple or forms.CheckboxSelectMultiple for multiple
    # How to have an all option? How to limit depending on category?
    min_price = forms.IntegerField(label='Minimum Price', min_value=0, initial=0)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, initial=500)
    available = forms.BooleanField(required=False)
