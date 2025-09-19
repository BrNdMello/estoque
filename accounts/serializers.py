from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User
    """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'nivel_acesso', 'telefone', 'ativo', 'data_criacao',
            'password', 'password_confirm'
        ]
        read_only_fields = ['id', 'data_criacao']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer para autenticação de usuários
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Usuário desativado.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Username e password são obrigatórios.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil do usuário (sem senha)
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'nivel_acesso', 'telefone', 'ativo', 'data_criacao'
        ]
        read_only_fields = ['id', 'username', 'data_criacao']

