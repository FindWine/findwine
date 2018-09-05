# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-05 13:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0032_auto_20180704_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='winegrape',
            options={'ordering': ['-percentage']},
        ),
        migrations.AddField(
            model_name='merchantwine',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wine',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wine',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='winevintage',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='winevintage',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
