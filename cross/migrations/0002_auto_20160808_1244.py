# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cross', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crosspicture',
            options={'ordering': ('datetime',)},
        ),
        migrations.AlterField(
            model_name='crosspicture',
            name='like_count',
            field=models.IntegerField(null=True, default=0),
        ),
        migrations.AlterField(
            model_name='crosspicture',
            name='picture',
            field=models.ImageField(blank=True, upload_to='cross_picture', null=True),
        ),
    ]
