# Generated by Django 2.2.2 on 2020-01-01 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20200102_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='family_name',
        ),
    ]