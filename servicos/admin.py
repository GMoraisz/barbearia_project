# servicos/admin.py
from django.contrib import admin
from .models import Servico

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'tipo', 'preco')  # Corrija aqui para usar 'preco', não 'valor'

admin.site.register(Servico, ServicoAdmin)
