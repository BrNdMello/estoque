from django.db import models
from accounts.models import User


class UBS(models.Model):
    """
    Modelo para Unidades Básicas de Saúde
    """
    nome = models.CharField(max_length=200, verbose_name='Nome da UBS')
    endereco = models.TextField(verbose_name='Endereço')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    cep = models.CharField(max_length=10, verbose_name='CEP')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ubs_responsavel',
        verbose_name='Responsável'
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'UBS'
        verbose_name_plural = 'UBSs'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"
    
    @property
    def endereco_completo(self):
        return f"{self.endereco}, {self.cidade}/{self.estado} - CEP: {self.cep}"