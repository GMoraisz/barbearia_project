from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{10,15}$', 'Digite apenas números válidos no telefone.')],
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.telefone}"
