from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import UBS
from .serializers import UBSSerializer, UBSListSerializer


class UBSListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria UBSs
    """
    queryset = UBS.objects.filter(ativo=True)
    serializer_class = UBSSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cidade', 'estado', 'ativo']
    search_fields = ['nome', 'cidade', 'estado', 'endereco']
    ordering_fields = ['nome', 'cidade', 'data_criacao']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UBSListSerializer
        return UBSSerializer


class UBSDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de UBS
    """
    queryset = UBS.objects.all()
    serializer_class = UBSSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - apenas desativa
        instance.ativo = False
        instance.save()