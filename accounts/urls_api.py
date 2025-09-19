from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='api-user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='api-user-detail'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('profile/', views.profile_view, name='api-profile'),
    path('profile/update/', views.update_profile_view, name='api-update-profile'),
]


