# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-07 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winterblog', '0002_auto_20171227_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(help_text='Enter comment for the blog', max_length=200, null=True),
        ),
    ]