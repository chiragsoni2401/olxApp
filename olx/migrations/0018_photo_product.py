# Generated by Django 2.1.5 on 2019-04-02 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0017_auto_20190402_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='olx.Product'),
        ),
    ]