# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-03 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_auto_20170602_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='uploaded_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='albums.UploadedFile'),
        ),
    ]