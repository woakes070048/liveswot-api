# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-31 23:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swot_item_vote', '0003_auto_20180330_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='+', to='swot_item.SwotItem'),
        ),
    ]
