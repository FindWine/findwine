# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-07 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0036_remove_winevintage_image_label_horizontal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winefoodpairing',
            name='strength',
            field=models.CharField(blank=True, choices=[('1', 'Perfect'), ('2', 'Ok')], default='2', max_length=2),
        ),
    ]
