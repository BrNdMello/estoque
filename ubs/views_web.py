from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UBS


@login_required
def ubs_list_view(request):
    """
    View para listagem de UBSs
    """
    ubs_list = UBS.objects.filter(ativo=True).select_related('responsavel')
    
    # Filtros
    search = request.GET.get('search', '')
    estado = request.GET.get('estado', '')
    status = request.GET.get('status', '')
    
    if search:
        ubs_list = ubs_list.filter(
            nome__icontains=search
        ) | ubs_list.filter(
            cidade__icontains=search
        )
    
    if estado:
        ubs_list = ubs_list.filter(estado=estado)
    
    if status == 'inativo':
        ubs_list = UBS.objects.filter(ativo=False)
    
    context = {
        'ubs_list': ubs_list,
        'search': search,
        'estado': estado,
        'status': status,
    }
    
    return render(request, 'ubs/list.html', context)

