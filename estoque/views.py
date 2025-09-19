from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import EstoqueMinimo, LoteMedicamento, MovimentacaoEstoque
from .serializers import (
    EstoqueMinimoSerializer, LoteMedicamentoSerializer, MovimentacaoEstoqueSerializer,
    EntradaEstoqueSerializer, SaidaEstoqueSerializer, TransferenciaEstoqueSerializer
)
from medicamentos.models import Medicamento
from ubs.models import UBS


class EstoqueMinimoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria configurações de estoque mínimo
    """
    queryset = EstoqueMinimo.objects.filter(ativo=True)
    serializer_class = EstoqueMinimoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medicamento', 'ubs', 'ativo']
    search_fields = ['medicamento__nome', 'ubs__nome']
    ordering_fields = ['medicamento__nome', 'ubs__nome', 'quantidade_minima']
    ordering = ['medicamento__nome']


class EstoqueMinimoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de estoque mínimo
    """
    queryset = EstoqueMinimo.objects.all()
    serializer_class = EstoqueMinimoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - apenas desativa
        instance.ativo = False
        instance.save()


class LoteMedicamentoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria lotes de medicamentos
    """
    queryset = LoteMedicamento.objects.filter(ativo=True)
    serializer_class = LoteMedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medicamento', 'ubs', 'ativo']
    search_fields = ['medicamento__nome', 'numero_lote', 'ubs__nome']
    ordering_fields = ['data_validade', 'numero_lote', 'medicamento__nome']
    ordering = ['data_validade']


class LoteMedicamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhes, atualização e exclusão de lote
    """
    queryset = LoteMedicamento.objects.all()
    serializer_class = LoteMedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - apenas desativa
        instance.ativo = False
        instance.save()


class MovimentacaoEstoqueListView(generics.ListAPIView):
    """
    Lista movimentações de estoque
    """
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'medicamento', 'ubs_origem', 'ubs_destino', 'usuario']
    search_fields = ['medicamento__nome', 'lote__numero_lote', 'observacoes']
    ordering_fields = ['data_movimentacao', 'medicamento__nome']
    ordering = ['-data_movimentacao']


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def entrada_estoque(request):
    """
    Endpoint para entrada de estoque
    """
    serializer = EntradaEstoqueSerializer(data=request.data)
    if serializer.is_valid():
        try:
            medicamento = Medicamento.objects.get(id=serializer.validated_data['medicamento'])
            ubs = UBS.objects.get(id=serializer.validated_data['ubs'])
            
            # Criar ou atualizar lote
            lote, created = LoteMedicamento.objects.get_or_create(
                medicamento=medicamento,
                ubs=ubs,
                numero_lote=serializer.validated_data['numero_lote'],
                data_validade=serializer.validated_data['data_validade'],
                defaults={
                    'quantidade_inicial': serializer.validated_data['quantidade'],
                    'quantidade_atual': 0,
                    'preco_unitario': serializer.validated_data.get('preco_unitario'),
                }
            )
            
            if not created:
                lote.quantidade_inicial += serializer.validated_data['quantidade']
                lote.save()
            
            # Criar movimentação
            movimentacao = MovimentacaoEstoque.objects.create(
                tipo='entrada',
                medicamento=medicamento,
                lote=lote,
                ubs_origem=ubs,
                quantidade=serializer.validated_data['quantidade'],
                observacoes=serializer.validated_data.get('observacoes', ''),
                usuario=request.user
            )
            
            return Response({
                'message': 'Entrada de estoque registrada com sucesso',
                'movimentacao': MovimentacaoEstoqueSerializer(movimentacao).data
            }, status=status.HTTP_201_CREATED)
            
        except (Medicamento.DoesNotExist, UBS.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def saida_estoque(request):
    """
    Endpoint para saída de estoque
    """
    serializer = SaidaEstoqueSerializer(data=request.data)
    if serializer.is_valid():
        try:
            lote = LoteMedicamento.objects.get(id=serializer.validated_data['lote'])
            
            if lote.quantidade_atual < serializer.validated_data['quantidade']:
                return Response({
                    'error': 'Quantidade insuficiente em estoque'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Criar movimentação
            movimentacao = MovimentacaoEstoque.objects.create(
                tipo='saida',
                medicamento=lote.medicamento,
                lote=lote,
                ubs_origem=lote.ubs,
                quantidade=serializer.validated_data['quantidade'],
                destino_detalhado=serializer.validated_data['destino_detalhado'],
                observacoes=serializer.validated_data.get('observacoes', ''),
                usuario=request.user
            )
            
            return Response({
                'message': 'Saída de estoque registrada com sucesso',
                'movimentacao': MovimentacaoEstoqueSerializer(movimentacao).data
            }, status=status.HTTP_201_CREATED)
            
        except LoteMedicamento.DoesNotExist:
            return Response({'error': 'Lote não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estoque_atual(request):
    """
    Endpoint para consultar estoque atual por UBS
    """
    ubs_id = request.query_params.get('ubs')
    medicamento_id = request.query_params.get('medicamento')
    
    queryset = LoteMedicamento.objects.filter(ativo=True, quantidade_atual__gt=0)
    
    if ubs_id:
        queryset = queryset.filter(ubs_id=ubs_id)
    if medicamento_id:
        queryset = queryset.filter(medicamento_id=medicamento_id)
    
    serializer = LoteMedicamentoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estoque_critico(request):
    """
    Endpoint para consultar estoque crítico (próximo do mínimo)
    """
    ubs_id = request.query_params.get('ubs')
    
    # Buscar configurações de estoque mínimo
    estoque_minimo = EstoqueMinimo.objects.filter(ativo=True)
    if ubs_id:
        estoque_minimo = estoque_minimo.filter(ubs_id=ubs_id)
    
    estoque_critico = []
    for config in estoque_minimo:
        # Buscar lotes ativos do medicamento na UBS
        lotes = LoteMedicamento.objects.filter(
            medicamento=config.medicamento,
            ubs=config.ubs,
            ativo=True
        ).aggregate(total=Sum('quantidade_atual'))
        
        total_estoque = lotes['total'] or 0
        
        if total_estoque <= config.quantidade_minima:
            estoque_critico.append({
                'medicamento': config.medicamento.nome_completo,
                'ubs': config.ubs.nome,
                'quantidade_atual': total_estoque,
                'quantidade_minima': config.quantidade_minima,
                'diferenca': total_estoque - config.quantidade_minima
            })
    
    return Response(estoque_critico)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicamentos_vencimento(request):
    """
    Endpoint para consultar medicamentos próximos do vencimento
    """
    dias = int(request.query_params.get('dias', 30))
    ubs_id = request.query_params.get('ubs')
    
    data_limite = timezone.now().date() + timedelta(days=dias)
    
    queryset = LoteMedicamento.objects.filter(
        ativo=True,
        quantidade_atual__gt=0,
        data_validade__lte=data_limite
    )
    
    if ubs_id:
        queryset = queryset.filter(ubs_id=ubs_id)
    
    serializer = LoteMedicamentoSerializer(queryset, many=True)
    return Response(serializer.data)