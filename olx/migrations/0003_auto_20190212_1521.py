# Generated by Django 2.1.5 on 2019-02-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0002_auto_20190212_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='height_field',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='width_field',
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.FileField(upload_to='photos/'),
        ),
    ]
