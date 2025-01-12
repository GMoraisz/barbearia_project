# utils.py
from .models import Agendamento

def horario_disponivel(data_agendamento):
    """
    Verifica se o horário está disponível.
    :param data_agendamento: Objeto datetime da data e hora solicitadas.
    :return: True se o horário está livre, False se está ocupado.
    """
    return not Agendamento.objects.filter(data=data_agendamento).exists()
