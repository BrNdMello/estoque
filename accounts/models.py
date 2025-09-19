from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo de usuário personalizado com níveis de acesso
    """
    NIVEL_ACESSO_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('visualizador', 'Visualizador'),
    ]
    
    nivel_acesso = models.CharField(
        max_length=20,
        choices=NIVEL_ACESSO_CHOICES,
        default='visualizador',
        verbose_name='Nível de Acesso'
    )
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_nivel_acesso_display()})"
    
    def is_admin(self):
        return self.nivel_acesso == 'admin'
    
    def is_operador(self):
        return self.nivel_acesso in ['admin', 'operador']
    
    def is_visualizador(self):
        return self.nivel_acesso in ['admin', 'operador', 'visualizador']