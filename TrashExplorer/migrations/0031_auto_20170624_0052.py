# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0030_auto_20170624_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinfo',
            name='trash_maximum_size',
            field=models.IntegerField(default=2000),
        ),
    ]
