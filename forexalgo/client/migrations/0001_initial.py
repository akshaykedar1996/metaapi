# Generated by Django 5.1.1 on 2024-12-14 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='db061f99', max_length=8, unique=True)),
                ('name_first', models.CharField(blank=True, max_length=50, null=True)),
                ('name_last', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('verify_code', models.CharField(blank=True, max_length=15, null=True)),
                ('date_joined', models.DateTimeField(default=None, verbose_name='date joined')),
                ('last_login', models.DateTimeField(default=None, verbose_name='last login')),
                ('status', models.BooleanField(default=False)),
                ('clint_status', models.CharField(blank=True, max_length=15, null=True)),
                ('mt5_login', models.CharField(blank=True, max_length=100, null=True)),
                ('mt5_password', models.CharField(blank=True, max_length=100, null=True)),
                ('mt5_server', models.CharField(blank=True, max_length=100, null=True)),
                ('api_key', models.CharField(max_length=10000)),
            ],
        ),
    ]