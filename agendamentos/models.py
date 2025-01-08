from django.db import models
from clientes.models import Cliente

class Agendamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    tipo_corte = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    data_horario = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('confirmado', 'Confirmado'),
            ('cancelado', 'Cancelado')
        ],
        default='pendente'
    )

    def __str__(self):
        return f"{self.cliente.nome} - {self.data_horario.strftime('%d/%m/%Y %H:%M')}"
