# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 08:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0016_auto_20170908_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wine',
            name='long_name',
        ),
    ]
