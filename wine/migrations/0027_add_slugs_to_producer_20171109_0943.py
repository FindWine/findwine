# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 09:43
from __future__ import unicode_literals

from django.db import migrations
from wine.util import generate_unique_producer_slug


def add_slugs(apps, schema_editor):
    """
    Adds slug fields to all the existing Producers
    """
    Producer = apps.get_model('wine', 'Producer')
    for producer in Producer.objects.all():
        if not producer.slug:
            # have to do this explicitly since overridden saves don't work in migrations
            # see: https://docs.djangoproject.com/en/1.8/topics/migrations/#historical-models
            producer.slug = generate_unique_producer_slug(producer)
            print('setting slug: {}'.format(producer.slug))
            producer.save()
        assert producer.slug


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0026_auto_20171109_0934'),
    ]

    operations = [
        migrations.RunPython(add_slugs)
    ]
