# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SwotItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('boardtype', models.CharField(
                    choices=[(b'strength', b'Strength'), (b'weakness', b'Weakness'), (b'opportunity', b'Opportunity'),
                             (b'threat', b'Threat')], max_length=11)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
