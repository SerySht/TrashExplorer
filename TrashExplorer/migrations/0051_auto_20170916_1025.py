# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-16 07:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TrashExplorer', '0050_auto_20170916_0328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskinfo',
            name='log_path',
        ),
        migrations.RemoveField(
            model_name='trashinfo',
            name='log_path',
        ),
    ]
