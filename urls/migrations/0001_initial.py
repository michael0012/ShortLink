# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-09 01:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeClicked', models.DateTimeField(auto_now_add=True)),
                ('referer', models.CharField(max_length=255)),
                ('user_agent', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_url', models.CharField(max_length=200)),
                ('short_url', models.CharField(max_length=8, unique=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_deactive', models.DateTimeField(null=True)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clickerprofile',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urls.Url'),
        ),
    ]
