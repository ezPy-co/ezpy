# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=63)),
                ('install_name', models.CharField(max_length=63)),
                ('version', models.FloatField()),
                ('website', models.URLField()),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'pip package',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TerminalPrompt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=63)),
                ('install_name', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='environmentprofile',
            name='packages',
            field=models.ManyToManyField(related_name='profiles', null=True, to='installer_config.Package', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='environmentprofile',
            name='prompt',
            field=models.ForeignKey(related_name='profile', to='installer_config.TerminalPrompt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='environmentprofile',
            name='user',
            field=models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
