# Generated by Django 3.0.2 on 2020-01-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Pharmacist', 'Pharmacist'), ('Technician', 'Technician')], max_length=10),
        ),
    ]