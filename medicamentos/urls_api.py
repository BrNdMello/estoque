from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.CategoriaMedicamentoListCreateView.as_view(), name='api-categoria-list-create'),
    path('categorias/<int:pk>/', views.CategoriaMedicamentoDetailView.as_view(), name='api-categoria-detail'),
    path('', views.MedicamentoListCreateView.as_view(), name='api-medicamento-list-create'),
    path('<int:pk>/', views.MedicamentoDetailView.as_view(), name='api-medicamento-detail'),
]


