# Generated by Django 2.1.5 on 2019-04-10 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0021_auto_20190410_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uploaded_by_id',
            field=models.IntegerField(default=0),
        ),
    ]
