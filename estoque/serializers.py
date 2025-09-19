from rest_framework import serializers
from .models import EstoqueMinimo, LoteMedicamento, MovimentacaoEstoque
from medicamentos.serializers import MedicamentoListSerializer
from ubs.serializers import UBSListSerializer
from accounts.serializers import UserProfileSerializer


class EstoqueMinimoSerializer(serializers.ModelSerializer):
    """
    Serializer para configuração de estoque mínimo
    """
    medicamento_nome = serializers.CharField(source='medicamento.nome_completo', read_only=True)
    ubs_nome = serializers.CharField(source='ubs.nome', read_only=True)
    
    class Meta:
        model = EstoqueMinimo
        fields = [
            'id', 'medicamento', 'medicamento_nome', 'ubs', 'ubs_nome',
            'quantidade_minima', 'ativo', 'data_criacao', 'data_atualizacao'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']


class LoteMedicamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para lotes de medicamentos
    """
    medicamento_nome = serializers.CharField(source='medicamento.nome_completo', read_only=True)
    ubs_nome = serializers.CharField(source='ubs.nome', read_only=True)
    dias_para_vencimento = serializers.IntegerField(read_only=True)
    proximo_vencimento = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = LoteMedicamento
        fields = [
            'id', 'medicamento', 'medicamento_nome', 'ubs', 'ubs_nome',
            'numero_lote', 'data_validade', 'quantidade_atual', 'quantidade_inicial',
            'preco_unitario', 'ativo', 'data_criacao', 'data_atualizacao',
            'dias_para_vencimento', 'proximo_vencimento'
        ]
        read_only_fields = ['id', 'quantidade_atual', 'data_criacao', 'data_atualizacao']


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para movimentações de estoque
    """
    medicamento_nome = serializers.CharField(source='medicamento.nome_completo', read_only=True)
    lote_numero = serializers.CharField(source='lote.numero_lote', read_only=True)
    ubs_origem_nome = serializers.CharField(source='ubs_origem.nome', read_only=True)
    ubs_destino_nome = serializers.CharField(source='ubs_destino.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id', 'tipo', 'medicamento', 'medicamento_nome', 'lote', 'lote_numero',
            'ubs_origem', 'ubs_origem_nome', 'ubs_destino', 'ubs_destino_nome',
            'quantidade', 'destino_detalhado', 'observacoes', 'usuario', 'usuario_nome',
            'data_movimentacao'
        ]
        read_only_fields = ['id', 'data_movimentacao']


class EntradaEstoqueSerializer(serializers.Serializer):
    """
    Serializer para entrada de estoque
    """
    medicamento = serializers.IntegerField()
    ubs = serializers.IntegerField()
    numero_lote = serializers.CharField(max_length=50)
    data_validade = serializers.DateField()
    quantidade = serializers.IntegerField(min_value=1)
    preco_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    observacoes = serializers.CharField(required=False, allow_blank=True)


class SaidaEstoqueSerializer(serializers.Serializer):
    """
    Serializer para saída de estoque
    """
    lote = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)
    destino_detalhado = serializers.ChoiceField(choices=MovimentacaoEstoque.DESTINO_CHOICES)
    observacoes = serializers.CharField(required=False, allow_blank=True)


class TransferenciaEstoqueSerializer(serializers.Serializer):
    """
    Serializer para transferência de estoque entre UBSs
    """
    lote_origem = serializers.IntegerField()
    ubs_destino = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)
    observacoes = serializers.CharField(required=False, allow_blank=True)

