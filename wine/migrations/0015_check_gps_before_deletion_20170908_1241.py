# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 12:41
from __future__ import unicode_literals

from django.db import migrations
from wine.geoposition import geoposition_to_dms_string


def check_gps_coordinates(apps, schema_editor):
    """
    Adds the Winemaker object in WineVintage.winemaker to the
    many-to-many relationship in WineVintage.winemakers
    """
    Producer = apps.get_model('wine', 'Producer')

    for producer in Producer.objects.all():
        if producer.coordinates_text:
            if producer.coordinates_google:
                print('\n==== {} ===='.format(producer.name))
                print('text:\t{}\ngoogle:\t{}'.format(producer.coordinates_text,
                                                      geoposition_to_dms_string(producer.coordinates_google)))
            else:
                raise Exception('Producer {} has text coordinates but no geoposition'.format(producer))


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0014_winevintage_description'),
    ]

    operations = [
        migrations.RunPython(check_gps_coordinates)
    ]