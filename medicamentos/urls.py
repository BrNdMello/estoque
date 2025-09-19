from django.urls import path
from . import views, views_web

web_urlpatterns = [
    path('', views_web.medicamento_list_view, name='medicamento-list'),
]

api_urlpatterns = [
    path('categorias/', views.CategoriaMedicamentoListCreateView.as_view(), name='api-categoria-list-create'),
    path('categorias/<int:pk>/', views.CategoriaMedicamentoDetailView.as_view(), name='api-categoria-detail'),
    path('', views.MedicamentoListCreateView.as_view(), name='api-medicamento-list-create'),
    path('<int:pk>/', views.MedicamentoDetailView.as_view(), name='api-medicamento-detail'),
]

urlpatterns = web_urlpatterns
