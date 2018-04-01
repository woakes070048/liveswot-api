# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-30 16:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swot',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', related_query_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
