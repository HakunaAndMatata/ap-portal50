# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 20:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0007_auto_20160625_1639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['num']},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['chapter__num', 'num']},
        ),
    ]
