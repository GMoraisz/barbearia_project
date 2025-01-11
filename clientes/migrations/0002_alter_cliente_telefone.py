# Generated by Django 5.1.4 on 2025-01-11 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^\\d{10,15}$', 'Digite apenas números válidos no telefone.')]),
        ),
    ]
