# servicos/models.py
from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, default='Serviço padrão')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add a default value here

    def __str__(self):
        return self.nome