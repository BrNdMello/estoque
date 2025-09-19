from django.urls import path
from . import views, views_web

web_urlpatterns = [
    path('', views_web.ubs_list_view, name='ubs-list'),
]

api_urlpatterns = [
    path('', views.UBSListCreateView.as_view(), name='api-ubs-list-create'),
    path('<int:pk>/', views.UBSDetailView.as_view(), name='api-ubs-detail'),
]

urlpatterns = web_urlpatterns

