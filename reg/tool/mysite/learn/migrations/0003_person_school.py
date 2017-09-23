# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='school',
            field=models.ForeignKey(default=datetime.datetime(2017, 8, 12, 6, 37, 42, 988551, tzinfo=utc), to='learn.School'),
            preserve_default=False,
        ),
    ]
