# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0002_auto_20170530_1226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodpairing',
            options={'ordering': ['category', 'name']},
        ),
        migrations.AlterField(
            model_name='foodpairing',
            name='category',
            field=models.CharField(choices=[('Meat', 'Meat'), ('Poultry', 'Poultry'), ('Seafood', 'Seafood'), ('Dairy', 'Dairy'), ('Vegetable', 'Vegetable'), ('Herb or Spice', 'Herb or Spice'), ('Starch', 'Starch'), ('Sweet', 'Sweet')], max_length=64),
        ),
    ]
