# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-21 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0005_auto_20170519_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='thumbnail',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
