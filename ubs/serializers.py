from rest_framework import serializers
from .models import UBS
from accounts.serializers import UserProfileSerializer


class UBSSerializer(serializers.ModelSerializer):
    """
    Serializer para UBS
    """
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = UBS
        fields = [
            'id', 'nome', 'endereco', 'cidade', 'estado', 'cep',
            'telefone', 'email', 'responsavel', 'responsavel_nome',
            'ativo', 'data_criacao', 'data_atualizacao', 'endereco_completo'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']


class UBSListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de UBSs
    """
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = UBS
        fields = [
            'id', 'nome', 'cidade', 'estado', 'responsavel_nome',
            'telefone', 'ativo', 'endereco_completo'
        ]

