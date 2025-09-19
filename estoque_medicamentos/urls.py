"""
URL configuration for estoque_medicamentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path('', redirect_to_dashboard),
    path('admin/', admin.site.urls),

    # Web URLs
    path('', include('accounts.urls')),
    path('medicamentos/', include('medicamentos.urls')),
    path('ubs/', include('ubs.urls')),
    path('estoque/', include('estoque.urls')),
    path('relatorios/', include('relatorios.urls')),

    # API URLs
    path('api/accounts/', include(('accounts.urls_api', 'accounts'), namespace='accounts-api')),
    path('api/medicamentos/', include(('medicamentos.urls_api', 'medicamentos'), namespace='medicamentos-api')),
    path('api/ubs/', include(('ubs.urls_api', 'ubs'), namespace='ubs-api')),
    path('api/estoque/', include(('estoque.urls_api', 'estoque'), namespace='estoque-api')),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
