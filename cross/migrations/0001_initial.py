# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrossPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('picture', models.ImageField(upload_to='cross_picture', blank=True)),
                ('datetime', models.DateTimeField()),
                ('time_str', models.CharField(max_length=100)),
                ('detail_url', models.CharField(max_length=255, blank=True, null=True)),
                ('detail_title', models.CharField(max_length=100, blank=True, null=True)),
                ('like_count', models.IntegerField(default=0)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('altitude', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('altitude', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='crosspicture',
            name='place',
            field=models.ForeignKey(to='cross.Place'),
        ),
    ]
