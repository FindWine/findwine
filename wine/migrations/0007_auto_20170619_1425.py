# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0006_auto_20170619_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='appellation_primary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Appellation'),
        ),
        migrations.AddField(
            model_name='winevintage',
            name='appellation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Appellation'),
        ),
    ]
