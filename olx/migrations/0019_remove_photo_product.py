# Generated by Django 2.1.5 on 2019-04-02 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0018_photo_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='product',
        ),
    ]
