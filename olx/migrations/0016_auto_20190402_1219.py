# Generated by Django 2.1.5 on 2019-04-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0015_auto_20190328_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.FileField(default='NoImage.jpg', upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.BigIntegerField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
