from django.utils.timezone import now
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Agendamento
from .serializers import AgendamentoSerializer
from .utils import horario_disponivel
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def create(self, request, *args, **kwargs):
        # Obtém a data do corpo da requisição
        data_agendamento_str = request.data.get('data')

        if not data_agendamento_str:
            return Response(
                {"error": "O campo 'data' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Tenta converter a data para datetime
        try:
            data_agendamento = parse_datetime(data_agendamento_str)
            if data_agendamento is None:
                raise ValueError("Formato inválido.")
        except ValueError:
            return Response(
                {"error": "Formato de data inválido. Use o formato: YYYY-MM-DD HH:MM."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se o horário está disponível (usando sua função `horario_disponivel`)
        if not horario_disponivel(data_agendamento):
            return Response(
                {"error": "Horário indisponível. Escolha outro horário."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cria uma cópia mutável de `request.data`
        data_mutable = request.data.copy()
        data_mutable['data'] = data_agendamento.isoformat()

        # Continua o fluxo padrão do create com a nova data
        serializer = self.get_serializer(data=data_mutable)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def horarios_disponiveis(self, request):
        # Filtra os agendamentos futuros
        hoje = now()
        agendamentos = Agendamento.objects.filter(data__date__gte=hoje.date())
        
        # Formata os dados em períodos
        resultado = {}
        data_solicitada = request.query_params.get("data", hoje.date().strftime('%Y-%m-%d'))
        data_selecionada = datetime.strptime(data_solicitada, '%Y-%m-%d').date()

        # Inicializa os períodos
        resultado = {
            "date": data_selecionada.strftime('%d/%m/%Y'),
            "morning": {
                "timeRange": "08h-12h",
                "appointments": [],
                "available": True
            },
            "afternoon": {
                "timeRange": "13h-18h",
                "appointments": [],
                "available": True
            },
            "night": {
                "timeRange": "18h-21h",
                "appointments": [],
                "available": True
            }
        }

        # Verifica a disponibilidade de cada período
        for agendamento in agendamentos.filter(data__date=data_selecionada):
            hora = agendamento.data
            cliente = agendamento.cliente.nome
            
            # Verifica os períodos
            if hora.hour >= 8 and hora.hour < 12:
                resultado["morning"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["morning"]["available"] = False  # Marca como indisponível
            elif hora.hour >= 13 and hora.hour < 18:
                resultado["afternoon"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["afternoon"]["available"] = False  # Marca como indisponível
            elif hora.hour >= 18 and hora.hour <= 21:
                resultado["night"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["night"]["available"] = False  # Marca como indisponível

        # Retorna a resposta com a disponibilidade
        return Response(resultado)
