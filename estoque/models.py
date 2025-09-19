from django.db import models
from django.core.validators import MinValueValidator
from medicamentos.models import Medicamento
from ubs.models import UBS
from accounts.models import User


class EstoqueMinimo(models.Model):
    """
    Configuração de estoque mínimo por medicamento e UBS
    """
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name='Medicamento'
    )
    ubs = models.ForeignKey(
        UBS,
        on_delete=models.CASCADE,
        verbose_name='UBS'
    )
    quantidade_minima = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade Mínima'
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Estoque Mínimo'
        verbose_name_plural = 'Estoques Mínimos'
        unique_together = ['medicamento', 'ubs']
    
    def __str__(self):
        return f"{self.medicamento} - {self.ubs} (Min: {self.quantidade_minima})"


class LoteMedicamento(models.Model):
    """
    Lotes de medicamentos com data de validade
    """
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name='Medicamento'
    )
    ubs = models.ForeignKey(
        UBS,
        on_delete=models.CASCADE,
        verbose_name='UBS'
    )
    numero_lote = models.CharField(max_length=50, verbose_name='Número do Lote')
    data_validade = models.DateField(verbose_name='Data de Validade')
    quantidade_atual = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantidade Atual'
    )
    quantidade_inicial = models.PositiveIntegerField(
        verbose_name='Quantidade Inicial'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço Unitário'
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lote de Medicamento'
        verbose_name_plural = 'Lotes de Medicamentos'
        ordering = ['data_validade', 'numero_lote']
    
    def __str__(self):
        return f"{self.medicamento} - Lote: {self.numero_lote} (Venc: {self.data_validade})"
    
    @property
    def dias_para_vencimento(self):
        from django.utils import timezone
        hoje = timezone.now().date()
        return (self.data_validade - hoje).days
    
    @property
    def proximo_vencimento(self):
        return self.dias_para_vencimento <= 30


class MovimentacaoEstoque(models.Model):
    """
    Registro de todas as movimentações de estoque
    """
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
        ('transferencia', 'Transferência'),
    ]
    
    DESTINO_CHOICES = [
        ('paciente', 'Paciente'),
        ('ubs', 'UBS'),
        ('descarte', 'Descarte'),
        ('transferencia', 'Transferência'),
    ]
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Movimentação'
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name='Medicamento'
    )
    lote = models.ForeignKey(
        LoteMedicamento,
        on_delete=models.CASCADE,
        verbose_name='Lote'
    )
    ubs_origem = models.ForeignKey(
        UBS,
        on_delete=models.CASCADE,
        related_name='movimentacoes_origem',
        verbose_name='UBS de Origem'
    )
    ubs_destino = models.ForeignKey(
        UBS,
        on_delete=models.CASCADE,
        related_name='movimentacoes_destino',
        blank=True,
        null=True,
        verbose_name='UBS de Destino'
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    destino_detalhado = models.CharField(
        max_length=20,
        choices=DESTINO_CHOICES,
        blank=True,
        null=True,
        verbose_name='Destino Detalhado'
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Usuário Responsável'
    )
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.medicamento} - {self.quantidade} unidades"
    
    def save(self, *args, **kwargs):
        # Salvar primeiro a movimentação
        super().save(*args, **kwargs)
        
        # Depois atualizar quantidade do lote
        if self.tipo == 'entrada':
            self.lote.quantidade_atual += self.quantidade
        elif self.tipo in ['saida', 'ajuste']:
            self.lote.quantidade_atual -= self.quantidade
        elif self.tipo == 'transferencia':
            self.lote.quantidade_atual -= self.quantidade
        
        self.lote.save()