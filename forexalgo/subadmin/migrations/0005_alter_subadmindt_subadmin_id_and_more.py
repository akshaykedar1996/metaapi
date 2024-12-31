# Generated by Django 5.1.1 on 2024-12-17 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0004_alter_subadmindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subadmindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='2a8887b9', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='subadmindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 18, 10, 32, 42, 740031, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
    ]
