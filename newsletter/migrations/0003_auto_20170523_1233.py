# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 18:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_join_session_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='join',
            old_name='email',
            new_name='user',
        ),
    ]
