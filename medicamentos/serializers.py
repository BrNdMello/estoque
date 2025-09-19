from rest_framework import serializers
from .models import CategoriaMedicamento, Medicamento


class CategoriaMedicamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para categorias de medicamentos
    """
    class Meta:
        model = CategoriaMedicamento
        fields = ['id', 'nome', 'descricao', 'ativo', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']


class MedicamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para medicamentos
    """
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    nome_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Medicamento
        fields = [
            'id', 'nome', 'principio_ativo', 'dosagem', 'unidade_medida',
            'categoria', 'categoria_nome', 'codigo_barras', 'descricao',
            'ativo', 'data_criacao', 'data_atualizacao', 'nome_completo'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    def validate_codigo_barras(self, value):
        if value and Medicamento.objects.filter(codigo_barras=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Já existe um medicamento com este código de barras.")
        return value


class MedicamentoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de medicamentos
    """
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    nome_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Medicamento
        fields = [
            'id', 'nome', 'principio_ativo', 'dosagem', 'unidade_medida',
            'categoria_nome', 'codigo_barras', 'ativo', 'nome_completo'
        ]

