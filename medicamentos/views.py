from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CategoriaMedicamento, Medicamento
from .serializers import (
    CategoriaMedicamentoSerializer, 
    MedicamentoSerializer, 
    MedicamentoListSerializer
)


class CategoriaMedicamentoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria categorias de medicamentos
    """
    queryset = CategoriaMedicamento.objects.filter(ativo=True)
    serializer_class = CategoriaMedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']
    ordering = ['nome']


class CategoriaMedicamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de categoria
    """
    queryset = CategoriaMedicamento.objects.all()
    serializer_class = CategoriaMedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - apenas desativa
        instance.ativo = False
        instance.save()


class MedicamentoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria medicamentos
    """
    queryset = Medicamento.objects.filter(ativo=True)
    serializer_class = MedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'ativo']
    search_fields = ['nome', 'principio_ativo', 'codigo_barras']
    ordering_fields = ['nome', 'data_criacao', 'data_atualizacao']
    ordering = ['nome']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MedicamentoListSerializer
        return MedicamentoSerializer


class MedicamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de medicamento
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - apenas desativa
        instance.ativo = False
        instance.save()