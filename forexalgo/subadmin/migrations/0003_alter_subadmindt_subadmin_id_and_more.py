# Generated by Django 5.1.1 on 2024-12-17 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0002_alter_subadmindt_subadmin_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subadmindt',
            name='subadmin_id',
            field=models.CharField(blank=True, default='37059dbe', max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='subadmindt',
            name='subadmin_last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 18, 8, 38, 47, 209088, tzinfo=datetime.timezone.utc), verbose_name='last login'),
        ),
    ]
