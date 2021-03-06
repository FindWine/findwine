# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0021_auto_20170911_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='google_place_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='currency',
            field=models.CharField(choices=[('ZAR', 'South Africa'), ('AUD', 'Australia'), ('GBP', 'United Kingdom'), ('USD', 'United States')], default='ZAR', max_length=3),
        ),
        migrations.AlterField(
            model_name='producer',
            name='tasting_currency',
            field=models.CharField(blank=True, choices=[('ZAR', 'South Africa'), ('AUD', 'Australia'), ('GBP', 'United Kingdom'), ('USD', 'United States')], default='ZAR', max_length=3, null=True),
        ),
    ]
