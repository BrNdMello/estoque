from django.urls import path
from . import views

urlpatterns = [
    path('minimo/', views.EstoqueMinimoListCreateView.as_view(), name='api-estoque-minimo-list-create'),
    path('minimo/<int:pk>/', views.EstoqueMinimoDetailView.as_view(), name='api-estoque-minimo-detail'),
    path('lotes/', views.LoteMedicamentoListCreateView.as_view(), name='api-lote-list-create'),
    path('lotes/<int:pk>/', views.LoteMedicamentoDetailView.as_view(), name='api-lote-detail'),
    path('movimentacoes/', views.MovimentacaoEstoqueListView.as_view(), name='api-movimentacao-list'),
    path('entrada/', views.entrada_estoque, name='api-entrada-estoque'),
    path('saida/', views.saida_estoque, name='api-saida-estoque'),
    path('atual/', views.estoque_atual, name='api-estoque-atual'),
    path('critico/', views.estoque_critico, name='api-estoque-critico'),
    path('vencimento/', views.medicamentos_vencimento, name='api-medicamentos-vencimento'),
]


