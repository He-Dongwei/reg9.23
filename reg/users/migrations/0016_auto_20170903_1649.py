# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 08:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artical', '0001_initial'),
        ('users', '0015_auto_20170903_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='accessrecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30, verbose_name='浏览人')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='访问时间')),
                ('page', models.URLField(verbose_name='访问页面')),
                ('IP', models.GenericIPAddressField(verbose_name='访问IP')),
                ('comment', models.CharField(max_length=255, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '上网记录',
                'verbose_name_plural': '上网记录',
            },
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyhead', models.CharField(max_length=255, verbose_name='发票抬头')),
                ('companynumber', models.CharField(max_length=30, verbose_name='单位纳税识别号')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='电话')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='地址')),
                ('bank', models.CharField(max_length=255, null=True, verbose_name='开户行')),
                ('accountnumber', models.CharField(max_length=30, null=True, verbose_name='开户账号')),
            ],
            options={
                'verbose_name': '发票单位',
                'verbose_name_plural': '发票单位',
            },
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paycompany', models.CharField(max_length=255, verbose_name='缴费单位名称')),
                ('paytime', models.DateTimeField(verbose_name='缴费时间')),
                ('paymoney', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='缴费金额')),
                ('payaccount', models.CharField(max_length=30, verbose_name='缴费账号')),
                ('comment', models.CharField(max_length=1000, verbose_name='备注')),
                ('creditfile', models.FileField(upload_to='', verbose_name='凭证文件')),
                ('paper', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artical.paper')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '缴费记录',
                'verbose_name_plural': '缴费记录',
            },
        ),
        migrations.RemoveField(
            model_name='internetrecord',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pay',
            name='user',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='accountnumber',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='address',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='billhead',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='user',
        ),
        migrations.AlterField(
            model_name='bill',
            name='billnumber',
            field=models.CharField(max_length=50, verbose_name='发票编号'),
        ),
        migrations.DeleteModel(
            name='Internetrecord',
        ),
        migrations.DeleteModel(
            name='pay',
        ),
        migrations.AddField(
            model_name='bill',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
        migrations.AddField(
            model_name='bill',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.payment'),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
    ]
