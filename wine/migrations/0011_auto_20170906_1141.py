# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0010_winevintage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='winevintage',
            name='winemakers',
            field=models.ManyToManyField(blank=True, related_name='winemakers', to='wine.Winemaker'),
        ),
        migrations.AlterField(
            model_name='winevintage',
            name='winemaker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winemaker', to='wine.Winemaker'),
        ),
    ]
