# Generated by Django 5.1.1 on 2024-12-17 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0004_alter_admindt_admin_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admindt',
            name='admin_id',
            field=models.CharField(blank=True, default='a1dd78ab', max_length=8, unique=True),
        ),
    ]
