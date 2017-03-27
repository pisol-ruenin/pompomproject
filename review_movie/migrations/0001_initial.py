# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('synopsis', models.CharField(max_length=1000)),
                ('released_date', models.DateField()),
                ('movie_image', models.CharField(max_length=1000)),
                ('genre', models.CharField(max_length=250)),
                ('director', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=1000)),
                ('score', models.IntegerField()),
                ('reviewer', models.CharField(max_length=100)),
                ('review_date', models.DateField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review_movie.Movie')),
            ],
        ),
    ]