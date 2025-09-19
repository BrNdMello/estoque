from django.contrib import admin
from .models import EstoqueMinimo, LoteMedicamento, MovimentacaoEstoque


@admin.register(EstoqueMinimo)
class EstoqueMinimoAdmin(admin.ModelAdmin):
    list_display = ['medicamento', 'ubs', 'quantidade_minima', 'ativo']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['medicamento__nome', 'ubs__nome']
    ordering = ['medicamento__nome']


@admin.register(LoteMedicamento)
class LoteMedicamentoAdmin(admin.ModelAdmin):
    list_display = ['medicamento', 'ubs', 'numero_lote', 'data_validade', 'quantidade_atual', 'ativo']
    list_filter = ['ubs', 'ativo', 'data_validade']
    search_fields = ['medicamento__nome', 'numero_lote', 'ubs__nome']
    ordering = ['-data_validade']
    fieldsets = (
        (None, {'fields': ('medicamento', 'ubs', 'numero_lote')}),
        ('Validade', {'fields': ('data_validade',)}),
        ('Quantidades', {'fields': ('quantidade_inicial', 'quantidade_atual')}),
        ('Financeiro', {'fields': ('preco_unitario',)}),
        ('Outros', {'fields': ('ativo',)}),
    )


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'medicamento', 'quantidade', 'ubs_origem', 'usuario', 'data_movimentacao']
    list_filter = ['tipo', 'data_movimentacao', 'ubs_origem']
    search_fields = ['medicamento__nome', 'lote__numero_lote', 'usuario__username']
    ordering = ['-data_movimentacao']
    readonly_fields = ['data_movimentacao']
    fieldsets = (
        (None, {'fields': ('tipo', 'medicamento', 'lote')}),
        ('Quantidade', {'fields': ('quantidade',)}),
        ('Locais', {'fields': ('ubs_origem', 'ubs_destino')}),
        ('Detalhes', {'fields': ('destino_detalhado', 'observacoes')}),
        ('Responsável', {'fields': ('usuario', 'data_movimentacao')}),
    )
