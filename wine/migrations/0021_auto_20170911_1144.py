# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0020_add_slugs_to_wine_vintage_20170911_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winevintage',
            name='slug',
            field=models.CharField(editable=False, max_length=191, unique=True),
        ),
    ]
