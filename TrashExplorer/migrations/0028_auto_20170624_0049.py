# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0027_remove_taskinfo_rename_when_name_conflict'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinfo',
            name='file_storage_time',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='taskinfo',
            name='trash_maximum_size',
            field=models.IntegerField(default=200),
        ),
    ]
