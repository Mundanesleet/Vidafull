# Generated by Django 5.1.2 on 2024-11-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0006_paciente_apellido_paciente_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='nota',
            field=models.TextField(blank=True, null=True),
        ),
    ]
