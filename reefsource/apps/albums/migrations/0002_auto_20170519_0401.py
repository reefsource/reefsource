# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-19 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='results',
            old_name='uploaded_file_id',
            new_name='uploaded_file',
        ),
        migrations.RenameField(
            model_name='uploadedfile',
            old_name='album_id',
            new_name='album',
        ),
    ]