# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0023_remove_trashinfo_config_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='trashinfo',
            name='dry',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='force',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='log_path',
            field=models.CharField(default='/home/sergey/smrm.log', max_length=500),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='rename_when_name_conflict',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='silent',
            field=models.BooleanField(default=False),
        ),
    ]
