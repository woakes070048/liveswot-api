# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-30 04:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swot_item_vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='swot_item.SwotItem'),
        ),
    ]
