from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'nivel_acesso', 'ativo']
    list_filter = ['nivel_acesso', 'ativo', 'data_criacao']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'telefone')}),
        ('Permissões', {'fields': ('nivel_acesso', 'ativo', 'is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined', 'data_criacao')}),
    )
