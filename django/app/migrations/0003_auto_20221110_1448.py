# Generated by Django 3.1.2 on 2022-11-10 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20221110_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='fast_lap',
            field=models.TimeField(null=False),
        ),
    ]
