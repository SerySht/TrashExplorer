# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0035_auto_20170821_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinfo',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trashinfo',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
    ]
