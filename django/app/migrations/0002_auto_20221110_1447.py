# Generated by Django 3.1.2 on 2022-11-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circuit',
            name='fast_lap',
        ),
        migrations.AddField(
            model_name='race',
            name='fast_lap',
            field=models.TimeField(null=True),
        ),
    ]