# Generated by Django 5.1.4 on 2025-01-11 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0002_remove_agendamento_preco_and_more'),
        ('clientes', '0002_alter_cliente_telefone'),
        ('servicos', '0003_servico_valor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agendamento',
            old_name='data_horario',
            new_name='data',
        ),
        migrations.RemoveField(
            model_name='agendamento',
            name='status',
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='servico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='servicos.servico'),
            preserve_default=False,
        ),
    ]