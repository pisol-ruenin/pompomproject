# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 12:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_movie', '0014_auto_20170418_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
