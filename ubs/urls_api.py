from django.urls import path
from . import views

urlpatterns = [
    path('', views.UBSListCreateView.as_view(), name='api-ubs-list-create'),
    path('<int:pk>/', views.UBSDetailView.as_view(), name='api-ubs-detail'),
]
