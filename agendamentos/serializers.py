from rest_framework import serializers
from .models import Agendamento
from servicos.models import Servico

class AgendamentoSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    servico_nome_e_preco = serializers.SerializerMethodField()  # Campo adicional formatado

    class Meta:
        model = Agendamento
        fields = ['id', 'cliente', 'cliente_nome', 'servico', 'servico_nome_e_preco', 'data']
        read_only_fields = ['id', 'cliente_nome', 'servico_nome_e_preco']

    def get_servico_nome_e_preco(self, obj):

        if obj.servico:
            return f"{obj.servico.nome} - R$ {obj.servico.preco:.2f}"
        return "Serviço não definido"