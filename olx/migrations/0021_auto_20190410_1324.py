# Generated by Django 2.1.5 on 2019-04-10 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0020_phototemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='uploaded_by_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='phototemp',
            name='uploaded_by_id',
            field=models.IntegerField(default=0),
        ),
    ]
