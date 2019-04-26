# Generated by Django 2.2 on 2019-04-26 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0006_call_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.OnCall'),
        ),
        migrations.AlterField(
            model_name='oncall',
            name='pharmacist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.Pharmacist'),
        ),
    ]
