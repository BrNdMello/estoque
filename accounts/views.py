from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer


class UserListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria usuários (apenas administradores)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return User.objects.all()
        elif user.is_operador():
            return User.objects.filter(nivel_acesso='visualizador')
        return User.objects.none()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de usuário
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return User.objects.all()
        elif user.is_operador():
            return User.objects.filter(nivel_acesso='visualizador')
        return User.objects.filter(id=user.id)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Endpoint para login de usuários
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
            'message': 'Login realizado com sucesso'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Endpoint para logout de usuários
    """
    try:
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    """
    Endpoint para obter perfil do usuário logado
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_view(request):
    """
    Endpoint para atualizar perfil do usuário logado
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)