# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-30 04:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swot', '0001_initial'),
        ('swot_item', '0007_auto_20180330_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='swotitem',
            name='swot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='swot.Swot'),
            preserve_default=False,
        ),
    ]
