# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0002_auto_20170604_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trashinfo',
            name='trash_config',
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='trash_config_path',
            field=models.CharField(default='/home/sergey/.smrm_congig', max_length=500),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='trash_path',
            field=models.CharField(default='/home/sergey/.smrm_congig', max_length=500),
        ),
    ]
