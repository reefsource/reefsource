# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-13 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_auto_20170612_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='success',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
