# Generated by Django 2.2.2 on 2020-01-05 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20200105_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Pharmacist', 'Pharmacist'), ('Pharmacy Technician', 'Pharmacy Technician')], max_length=19),
        ),
    ]
