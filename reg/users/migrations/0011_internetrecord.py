# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 07:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20170825_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internetrecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='访问时间')),
                ('page', models.URLField(verbose_name='访问页面')),
                ('IP', models.GenericIPAddressField(verbose_name='访问IP')),
                ('comment', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
