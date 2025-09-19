from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LoteMedicamento, EstoqueMinimo
from medicamentos.models import Medicamento
from ubs.models import UBS
from django.db.models import Sum, Count


@login_required
def estoque_atual_view(request):
    """
    View para estoque atual
    """
    lotes = LoteMedicamento.objects.filter(
        ativo=True, 
        quantidade_atual__gt=0
    ).select_related('medicamento', 'ubs', 'medicamento__categoria')
    
    # Filtros
    ubs_id = request.GET.get('ubs', '')
    medicamento_search = request.GET.get('medicamento', '')
    status = request.GET.get('status', '')
    
    if ubs_id:
        lotes = lotes.filter(ubs_id=ubs_id)
    
    if medicamento_search:
        lotes = lotes.filter(
            medicamento__nome__icontains=medicamento_search
        )
    
    if status == 'critico':
        # Buscar lotes com estoque crítico
        estoque_critico_ids = []
        for config in EstoqueMinimo.objects.filter(ativo=True):
            total_estoque = LoteMedicamento.objects.filter(
                medicamento=config.medicamento,
                ubs=config.ubs,
                ativo=True
            ).aggregate(total=Sum('quantidade_atual'))['total'] or 0
            
            if total_estoque <= config.quantidade_minima:
                estoque_critico_ids.extend(
                    LoteMedicamento.objects.filter(
                        medicamento=config.medicamento,
                        ubs=config.ubs,
                        ativo=True
                    ).values_list('id', flat=True)
                )
        
        lotes = lotes.filter(id__in=estoque_critico_ids)
    
    # Estatísticas
    total_lotes = lotes.count()
    estoque_critico_count = 0
    vencendo_count = 0
    
    for lote in lotes:
        # Verificar se está crítico
        try:
            config = EstoqueMinimo.objects.get(
                medicamento=lote.medicamento,
                ubs=lote.ubs,
                ativo=True
            )
            if lote.quantidade_atual <= config.quantidade_minima:
                estoque_critico_count += 1
        except EstoqueMinimo.DoesNotExist:
            pass
        
        # Verificar se está vencendo (30 dias)
        from datetime import timedelta
        from django.utils import timezone
        if lote.data_validade <= timezone.now().date() + timedelta(days=30):
            vencendo_count += 1
    
    em_dia_count = total_lotes - estoque_critico_count - vencendo_count
    
    context = {
        'lotes': lotes,
        'ubs_list': UBS.objects.filter(ativo=True),
        'total_lotes': total_lotes,
        'estoque_critico_count': estoque_critico_count,
        'vencendo_count': vencendo_count,
        'em_dia_count': em_dia_count,
        'ubs_id': ubs_id,
        'medicamento_search': medicamento_search,
        'status': status,
    }
    
    return render(request, 'estoque/atual.html', context)

