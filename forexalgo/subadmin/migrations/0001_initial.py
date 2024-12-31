# Generated by Django 5.1.1 on 2024-12-14 05:13

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subadmin_client_limit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subadmin_limit', models.CharField(max_length=20)),
                ('max_quantity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubAdminDT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subadmin_id', models.CharField(blank=True, default='2effd363', max_length=8, unique=True)),
                ('subadmin_name_first', models.CharField(blank=True, max_length=50, null=True)),
                ('subadmin_name_last', models.CharField(blank=True, max_length=50, null=True)),
                ('subadmin_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subadmin_password', models.CharField(blank=True, max_length=50, null=True)),
                ('subadmin_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('subadmin_verify_code', models.CharField(blank=True, max_length=15, null=True)),
                ('subadmin_keyword', models.CharField(blank=True, max_length=1000, null=True)),
                ('subadmin_logo', models.ImageField(blank=True, null=True, upload_to='photos/subadmin_logo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('subadmin_status', models.BooleanField(blank=True, default=False, null=True)),
                ('subadmin_date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('subadmin_last_login', models.DateTimeField(default=datetime.datetime(2024, 12, 15, 5, 13, 55, 989351, tzinfo=datetime.timezone.utc), verbose_name='last login')),
                ('subadmin_client_limit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subadmin.subadmin_client_limit')),
            ],
        ),
    ]
