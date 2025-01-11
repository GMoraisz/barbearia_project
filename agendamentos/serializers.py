from rest_framework import serializers
from .models import Agendamento
from servicos.serializers import ServicoSerializer
from clientes.models import Cliente
from servicos.models import Servico


class AgendamentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)  # Mostra o nome do cliente
    servico = serializers.PrimaryKeyRelatedField(queryset=Servico.objects.all())  # Permite selecionar o serviço por ID
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())  # Permite selecionar o cliente por ID

    class Meta:
        model = Agendamento
        fields = ['id', 'cliente', 'cliente_nome', 'servico', 'data']  # Campos do serializer
        read_only_fields = ['id', 'cliente_nome']  # Define campos somente leitura
