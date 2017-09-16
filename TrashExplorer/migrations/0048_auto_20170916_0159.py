# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 22:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0047_auto_20170915_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinfo',
            name='trash_maximum_size',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]