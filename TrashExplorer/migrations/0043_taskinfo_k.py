# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0042_auto_20170904_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinfo',
            name='k',
            field=models.FilePathField(default='kek'),
        ),
    ]
