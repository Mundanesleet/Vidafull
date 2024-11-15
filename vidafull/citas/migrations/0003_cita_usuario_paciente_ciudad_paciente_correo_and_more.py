# Generated by Django 5.1.2 on 2024-11-07 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0002_alter_cita_disponibilidad'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paciente',
            name='ciudad',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='paciente',
            name='correo',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='paciente',
            name='direccion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='paciente',
            name='edificio',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='paciente',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
