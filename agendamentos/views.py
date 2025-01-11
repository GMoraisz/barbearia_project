from django.utils.timezone import now
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Agendamento
from .serializers import AgendamentoSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

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
