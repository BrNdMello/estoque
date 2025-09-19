from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def relatorios_view(request):
    """
    View para página de relatórios
    """
    return render(request, 'relatorios/index.html')