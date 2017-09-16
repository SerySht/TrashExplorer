# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 00:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0049_auto_20170916_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinfo',
            name='file_storage_time',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2147483645)]),
        ),
        migrations.AlterField(
            model_name='taskinfo',
            name='trash_maximum_size',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2147483645)]),
        ),
        migrations.AlterField(
            model_name='trashinfo',
            name='file_storage_time',
            field=models.IntegerField(default=7, validators=[django.core.validators.MaxValueValidator(2147483645)]),
        ),
        migrations.AlterField(
            model_name='trashinfo',
            name='trash_maximum_size',
            field=models.IntegerField(default=200000, validators=[django.core.validators.MaxValueValidator(2147483645)]),
        ),
    ]
