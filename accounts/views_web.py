from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User


def login_view(request):
    """
    View para página de login
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    View para logout
    """
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    View para dashboard principal
    """
    # Estatísticas básicas
    from medicamentos.models import Medicamento
    from ubs.models import UBS
    from estoque.models import LoteMedicamento, MovimentacaoEstoque
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Contadores gerais
    total_medicamentos = Medicamento.objects.filter(ativo=True).count()
    total_ubs = UBS.objects.filter(ativo=True).count()
    
    # Estoque atual
    estoque_atual = LoteMedicamento.objects.filter(
        ativo=True, 
        quantidade_atual__gt=0
    ).aggregate(
        total_lotes=Count('id'),
        total_medicamentos=Sum('quantidade_atual')
    )
    
    # Medicamentos próximos do vencimento (30 dias)
    data_limite = datetime.now().date() + timedelta(days=30)
    medicamentos_vencendo = LoteMedicamento.objects.filter(
        ativo=True,
        quantidade_atual__gt=0,
        data_validade__lte=data_limite
    ).count()
    
    # Movimentações do mês
    inicio_mes = datetime.now().replace(day=1).date()
    movimentacoes_mes = MovimentacaoEstoque.objects.filter(
        data_movimentacao__date__gte=inicio_mes
    ).count()
    
    # Estoque crítico
    from estoque.models import EstoqueMinimo
    estoque_critico = []
    for config in EstoqueMinimo.objects.filter(ativo=True):
        total_estoque = LoteMedicamento.objects.filter(
            medicamento=config.medicamento,
            ubs=config.ubs,
            ativo=True
        ).aggregate(total=Sum('quantidade_atual'))['total'] or 0
        
        if total_estoque <= config.quantidade_minima:
            estoque_critico.append({
                'medicamento': config.medicamento.nome_completo,
                'ubs': config.ubs.nome,
                'quantidade_atual': total_estoque,
                'quantidade_minima': config.quantidade_minima
            })
    
    # Movimentações recentes
    movimentacoes_recentes = MovimentacaoEstoque.objects.select_related(
        'medicamento', 'ubs_origem', 'usuario'
    ).order_by('-data_movimentacao')[:10]
    
    context = {
        'total_medicamentos': total_medicamentos,
        'total_ubs': total_ubs,
        'total_lotes': estoque_atual['total_lotes'] or 0,
        'total_medicamentos_estoque': estoque_atual['total_medicamentos'] or 0,
        'medicamentos_vencendo': medicamentos_vencendo,
        'movimentacoes_mes': movimentacoes_mes,
        'estoque_critico': estoque_critico[:5],  # Top 5
        'movimentacoes_recentes': movimentacoes_recentes,
    }
    
    return render(request, 'dashboard.html', context)

