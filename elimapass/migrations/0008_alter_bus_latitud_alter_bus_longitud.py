# Generated by Django 5.1.1 on 2024-10-31 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elimapass', '0007_alter_bus_latitud_alter_bus_longitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='bus',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
