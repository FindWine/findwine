# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-30 15:43
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0030_merchantwine_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='affiliate_params',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]