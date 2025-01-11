from rest_framework import serializers
from .models import Cliente
from django.core.validators import RegexValidator

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    telefone = serializers.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{10,15}$', 'Digite apenas números válidos no telefone.')]
    )
