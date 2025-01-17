# Generated by Django 5.1.4 on 2025-01-08 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_corte', models.CharField(max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=6)),
                ('data_horario', models.DateTimeField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='clientes.cliente')),
            ],
        ),
    ]
