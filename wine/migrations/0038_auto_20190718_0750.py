# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-18 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wine', '0037_auto_20190607_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(help_text='2 digit ISO e.g. ZA for South Africa', max_length=2)),
                ('currency_name', models.CharField(blank=True, max_length=256, null=True)),
                ('currency_code', models.CharField(help_text='3 digit ISO e.g. ZAR for South Africa', max_length=3)),
                ('currency_symbol', models.CharField(blank=True, max_length=1, null=True)),
                ('is_producer', models.NullBooleanField(help_text='No for a country that should not show up in Wine Vintage choices')),
                ('is_merchant', models.NullBooleanField(help_text='Yes to add a country that should show up in Merchant choices')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('last_modified_by', models.CharField(blank=True, default='', max_length=100)),
                ('name', models.CharField(max_length=191)),
            ],
            options={
                'ordering': ['producer', 'name'],
            },
        ),
        migrations.AlterField(
            model_name='appellation',
            name='country',
            field=models.CharField(choices=[('ZA', 'South Africa'), ('AR', 'Argentina'), ('AU', 'Australia'), ('CL', 'Chile'), ('CN', 'China'), ('FR', 'France'), ('IT', 'Italy'), ('LB', 'Lebanon'), ('NZ', 'New Zealand'), ('PT', 'Portugal'), ('ES', 'Spain'), ('GB', 'United Kingdom'), ('US', 'United States')], default='ZA', max_length=2),
        ),
        migrations.AlterField(
            model_name='producer',
            name='address',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='producer',
            name='appellation_primary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Appellation'),
        ),
        migrations.AlterField(
            model_name='producer',
            name='country',
            field=models.CharField(choices=[('ZA', 'South Africa'), ('AR', 'Argentina'), ('AU', 'Australia'), ('CL', 'Chile'), ('CN', 'China'), ('FR', 'France'), ('IT', 'Italy'), ('LB', 'Lebanon'), ('NZ', 'New Zealand'), ('PT', 'Portugal'), ('ES', 'Spain'), ('GB', 'United Kingdom'), ('US', 'United States')], default='ZA', max_length=2),
        ),
        migrations.AddField(
            model_name='range',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wine.Producer'),
        ),
        migrations.AddField(
            model_name='appellation',
            name='country_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Country'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='country_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Country'),
        ),
        migrations.AddField(
            model_name='merchantwine',
            name='country_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Country'),
        ),
        migrations.AddField(
            model_name='producer',
            name='country_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Country'),
        ),
        migrations.AddField(
            model_name='wine',
            name='range',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wine.Range'),
        ),
        migrations.AlterUniqueTogether(
            name='range',
            unique_together=set([('producer', 'name')]),
        ),
    ]
