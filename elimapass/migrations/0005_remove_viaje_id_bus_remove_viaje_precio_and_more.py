# Generated by Django 5.1.1 on 2024-10-03 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elimapass', '0004_alter_usuario_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viaje',
            name='id_bus',
        ),
        migrations.RemoveField(
            model_name='viaje',
            name='precio',
        ),
        migrations.AddField(
            model_name='viaje',
            name='precio_final',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('precio_base', models.FloatField()),
                ('id_ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elimapass.ruta')),
            ],
        ),
        migrations.AddField(
            model_name='viaje',
            name='id_tarifa',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='elimapass.tarifa'),
            preserve_default=False,
        ),
    ]