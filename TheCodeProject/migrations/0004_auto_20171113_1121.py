# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheCodeProject', '0003_codes_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codes',
            name='username',
            field=models.TextField(),
        ),
    ]