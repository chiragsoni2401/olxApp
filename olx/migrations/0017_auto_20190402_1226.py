# Generated by Django 2.1.5 on 2019-04-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0016_auto_20190402_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='contact',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
