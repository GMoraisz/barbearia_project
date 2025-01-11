# barbearia_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes.views import ClienteViewSet
from agendamentos.views import AgendamentoViewSet
from servicos.views import ServicoViewSet  # Importe o ServicoViewSet aqui

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'agendamentos', AgendamentoViewSet)
router.register(r'servicos', ServicoViewSet)  # Registre a view de serviços

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Inclua as rotas da API
]
