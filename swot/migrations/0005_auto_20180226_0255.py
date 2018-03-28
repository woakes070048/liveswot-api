# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-26 02:55
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('swot', '0004_change_name_swot_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('voteType', models.CharField(choices=[(b'up', b'UP'), (b'down', b'DOWN')], max_length=4)),
            ],
        ),
        migrations.RemoveField(
            model_name='upvote',
            name='item',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='boardtype',
            new_name='cardType',
        ),
        migrations.DeleteModel(
            name='UpVote',
        ),
        migrations.AddField(
            model_name='vote',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='swot.Item'),
        ),
    ]
