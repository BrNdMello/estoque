from django.contrib import admin
from .models import UBS


@admin.register(UBS)
class UBSAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado', 'responsavel', 'ativo']
    list_filter = ['estado', 'ativo', 'data_criacao']
    search_fields = ['nome', 'cidade', 'endereco', 'responsavel__username']
    ordering = ['nome']
    fieldsets = (
        (None, {'fields': ('nome', 'responsavel')}),
        ('Endereço', {'fields': ('endereco', 'cidade', 'estado', 'cep')}),
        ('Contato', {'fields': ('telefone', 'email')}),
        ('Outros', {'fields': ('ativo',)}),
    )
