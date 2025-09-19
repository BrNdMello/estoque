from django.contrib import admin
from .models import CategoriaMedicamento, Medicamento


@admin.register(CategoriaMedicamento)
class CategoriaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'principio_ativo', 'dosagem', 'unidade_medida', 'categoria', 'ativo']
    list_filter = ['categoria', 'unidade_medida', 'ativo', 'data_criacao']
    search_fields = ['nome', 'principio_ativo', 'codigo_barras']
    ordering = ['nome']
    fieldsets = (
        (None, {'fields': ('nome', 'principio_ativo')}),
        ('Dosagem', {'fields': ('dosagem', 'unidade_medida')}),
        ('Categoria', {'fields': ('categoria',)}),
        ('Identificação', {'fields': ('codigo_barras',)}),
        ('Outros', {'fields': ('descricao', 'ativo')}),
    )
