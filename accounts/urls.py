from django.urls import path
from . import views, views_web

web_urlpatterns = [
    path('login/', views_web.login_view, name='login'),
    path('logout/', views_web.logout_view, name='logout'),
    path('dashboard/', views_web.dashboard_view, name='dashboard'),
]

api_urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='api-user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='api-user-detail'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('profile/', views.profile_view, name='api-profile'),
    path('profile/update/', views.update_profile_view, name='api-update-profile'),
]

urlpatterns = web_urlpatterns
