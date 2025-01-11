from django.db import models
from servicos.models import Servico

class Agendamento(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateTimeField() 
    def __str__(self):
        return f"Agendamento para {self.cliente.nome} - {self.servico.nome} no dia {self.data.strftime('%d/%m/%Y %H:%M')}"
