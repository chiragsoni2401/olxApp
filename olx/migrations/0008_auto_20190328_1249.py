# Generated by Django 2.1.5 on 2019-03-28 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0007_auto_20190328_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.FileField(default='/media/photos/No_Image_Available.jpg', upload_to='photos/'),
        ),
    ]