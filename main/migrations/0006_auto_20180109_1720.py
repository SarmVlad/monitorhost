# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-09 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180109_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_code',
            field=models.CharField(default='7A73u3rcpmznvU2cadgS', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='img/profile_photo/default.png', upload_to='img/profile_photo/'),
        ),
    ]
