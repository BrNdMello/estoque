from django.db import models


class CategoriaMedicamento(models.Model):
    """
    Categorias de medicamentos (antibióticos, analgésicos, etc.)
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria de Medicamento'
        verbose_name_plural = 'Categorias de Medicamentos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    """
    Modelo para cadastro de medicamentos
    """
    UNIDADE_CHOICES = [
        ('mg', 'Miligrama (mg)'),
        ('g', 'Grama (g)'),
        ('ml', 'Mililitro (ml)'),
        ('l', 'Litro (l)'),
        ('un', 'Unidade'),
        ('cx', 'Caixa'),
        ('amp', 'Ampola'),
        ('frasco', 'Frasco'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name='Nome do Medicamento')
    principio_ativo = models.CharField(max_length=200, verbose_name='Princípio Ativo')
    dosagem = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Dosagem')
    unidade_medida = models.CharField(
        max_length=10,
        choices=UNIDADE_CHOICES,
        verbose_name='Unidade de Medida'
    )
    categoria = models.ForeignKey(
        CategoriaMedicamento,
        on_delete=models.PROTECT,
        verbose_name='Categoria'
    )
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nome']
        unique_together = ['nome', 'dosagem', 'unidade_medida']
    
    def __str__(self):
        return f"{self.nome} {self.dosagem}{self.unidade_medida}"
    
    @property
    def nome_completo(self):
        return f"{self.nome} {self.dosagem}{self.unidade_medida}"