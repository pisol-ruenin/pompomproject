# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_movie', '0022_reviewerrequest_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='job',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(blank=True, default='default/defult_profile.png', upload_to=''),
        ),
    ]
