from django.db import models
from servicos.models import Servico

class Agendamento(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateTimeField()  # Campo de data e hora

    def __str__(self):
        # Ajustando a exibição para evitar possíveis erros com formatos de data
        return f"Agendamento para {self.cliente.nome} - {self.servico.nome} no dia {self.data.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        # Define o formato padrão de exibição do campo `data` ao salvar ou acessar
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data']  # Ordena os agendamentos pela data
