from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Medicamento, CategoriaMedicamento


@login_required
def medicamento_list_view(request):
    """
    View para listagem de medicamentos
    """
    medicamentos = Medicamento.objects.filter(ativo=True).select_related('categoria')
    categorias = CategoriaMedicamento.objects.filter(ativo=True)
    
    # Filtros
    search = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')
    status = request.GET.get('status', '')
    
    if search:
        medicamentos = medicamentos.filter(
            nome__icontains=search
        ) | medicamentos.filter(
            principio_ativo__icontains=search
        )
    
    if categoria_id:
        medicamentos = medicamentos.filter(categoria_id=categoria_id)
    
    if status == 'inativo':
        medicamentos = Medicamento.objects.filter(ativo=False)
    
    context = {
        'medicamentos': medicamentos,
        'categorias': categorias,
        'search': search,
        'categoria_id': categoria_id,
        'status': status,
    }
    
    return render(request, 'medicamentos/list.html', context)

