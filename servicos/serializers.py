from rest_framework import serializers
from servicos.models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'preco']  # Inclui id, nome e preço do serviço
