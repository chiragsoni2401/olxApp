# Generated by Django 2.1.5 on 2019-04-26 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0023_auto_20190415_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='reference_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='olx.Product'),
        ),
    ]
