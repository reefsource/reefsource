# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-15 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_result_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.DecimalField(decimal_places=12, max_digits=16, null=True),
        ),
    ]