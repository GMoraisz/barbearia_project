from django.utils.timezone import now
from datetime import datetime, timedelta
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Agendamento
from .serializers import AgendamentoSerializer
from django.utils.dateparse import parse_datetime
from rest_framework import status

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
        if not self.horario_disponivel(data_agendamento):
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

        # Verifica os agendamentos e atualiza a disponibilidade
        for agendamento in agendamentos.filter(data__date=data_selecionada):
            hora = agendamento.data
            cliente = agendamento.cliente.nome

            # Marca como ocupado se houver agendamento no mesmo horário
            if hora.hour >= 8 and hora.hour < 12:
                resultado["morning"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["morning"]["available"] = False
            elif hora.hour >= 13 and hora.hour < 18:
                resultado["afternoon"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["afternoon"]["available"] = False
            elif hora.hour >= 18 and hora.hour < 21:
                resultado["night"]["appointments"].append({
                    "time": hora.strftime('%H:%M'),
                    "client": cliente
                })
                resultado["night"]["available"] = False

        # Verifica os horários disponíveis de 1 em 1 hora
        for periodo, info in resultado.items():
            if periodo in ["morning", "afternoon", "night"]:
                horarios = []
                start, end = 0, 0
                if periodo == "morning":
                    start, end = 8, 12
                elif periodo == "afternoon":
                    start, end = 13, 18
                elif periodo == "night":
                    start, end = 18, 21

                for hora in range(start, end):
                    horario_atual = datetime.combine(data_selecionada, datetime.min.time()) + timedelta(hours=hora)

                    # Verifica se já há agendamentos no horário
                    ocupado = agendamentos.filter(data__hour=hora, data__date=data_selecionada).exists()

                    # Adiciona o horário somente se ele não estiver ocupado
                    horarios.append({
                        "time": horario_atual.strftime('%H:%M'),
                        "available": not ocupado
                    })

                resultado[periodo]["appointments"] = horarios
                resultado[periodo]["available"] = any(appointment["available"] for appointment in horarios)

        # Retorna a resposta com a disponibilidade
        return Response(resultado)

    def horario_disponivel(self, data_agendamento):
        # Verifica se o horário já está ocupado (sem levar em conta os minutos)
        hora = data_agendamento.hour
        dia = data_agendamento.date()

        if Agendamento.objects.filter(data__hour=hora, data__date=dia).exists():
            return False

        return True

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        # Deleta todos os agendamentos
        Agendamento.objects.all().delete()

        return Response({"message": "Todos os agendamentos foram deletados com sucesso!"}, status=status.HTTP_204_NO_CONTENT)
