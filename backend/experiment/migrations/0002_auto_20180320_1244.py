# Generated by Django 2.0.1 on 2018-03-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='treatment',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assigned_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
