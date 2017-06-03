# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import reefsource.apps.albums.models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0009_album_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='thumbnail_labeled',
            field=models.FileField(max_length=255, null=True, upload_to=reefsource.apps.albums.models.uploaded_file_to),
        ),
    ]