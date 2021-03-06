# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0033_auto_20170821_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinfo',
            name='file_storage_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='info_message',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='log_path',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='operation_type',
            field=models.CharField(choices=[('simple delete', 'simple delete'), ('delete by regex', 'delete by regex')], max_length=50),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='regex',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='trash_maximum_size',
            field=models.IntegerField(),
        ),
    ]
