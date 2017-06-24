# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0018_auto_20170623_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinfo',
            name='regex',
            field=models.CharField(default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='operation_type',
            field=models.CharField(choices=[('simple delete', 'simple delete'), ('delete by regex', 'delete by regex')], default=None, max_length=50),
        ),
    ]
