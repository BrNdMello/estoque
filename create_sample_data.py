#!/usr/bin/env python
"""
Script para criar dados de exemplo no sistema de estoque de medicamentos
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_medicamentos.settings')
django.setup()

from accounts.models import User
from medicamentos.models import CategoriaMedicamento, Medicamento
from ubs.models import UBS
from estoque.models import EstoqueMinimo, LoteMedicamento
from django.utils import timezone
from datetime import timedelta

def create_sample_data():
    print("Criando dados de exemplo...")
    
    # Criar usuários de exemplo
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            nivel_acesso='admin'
        )
        print("✓ Usuário admin criado")
    else:
        admin = User.objects.get(username='admin')
        print("✓ Usuário admin já existe")
    
    if not User.objects.filter(username='operador1').exists():
        operador1 = User.objects.create_user(
            username='operador1',
            email='operador1@example.com',
            password='operador123',
            first_name='João',
            last_name='Silva',
            nivel_acesso='operador'
        )
        print("✓ Usuário operador1 criado")
    else:
        operador1 = User.objects.get(username='operador1')
        print("✓ Usuário operador1 já existe")
    
    # Criar categorias de medicamentos
    categorias_data = [
        {'nome': 'Antibióticos', 'descricao': 'Medicamentos antibióticos'},
        {'nome': 'Analgésicos', 'descricao': 'Medicamentos para dor'},
        {'nome': 'Anti-inflamatórios', 'descricao': 'Medicamentos anti-inflamatórios'},
        {'nome': 'Antitérmicos', 'descricao': 'Medicamentos para febre'},
        {'nome': 'Antialérgicos', 'descricao': 'Medicamentos para alergia'},
    ]
    
    for cat_data in categorias_data:
        categoria, created = CategoriaMedicamento.objects.get_or_create(
            nome=cat_data['nome'],
            defaults=cat_data
        )
        if created:
            print(f"✓ Categoria {categoria.nome} criada")
    
    # Criar medicamentos
    medicamentos_data = [
        {
            'nome': 'Amoxicilina',
            'principio_ativo': 'Amoxicilina',
            'dosagem': 500,
            'unidade_medida': 'mg',
            'categoria': 'Antibióticos'
        },
        {
            'nome': 'Dipirona',
            'principio_ativo': 'Dipirona Sódica',
            'dosagem': 500,
            'unidade_medida': 'mg',
            'categoria': 'Analgésicos'
        },
        {
            'nome': 'Ibuprofeno',
            'principio_ativo': 'Ibuprofeno',
            'dosagem': 400,
            'unidade_medida': 'mg',
            'categoria': 'Anti-inflamatórios'
        },
        {
            'nome': 'Paracetamol',
            'principio_ativo': 'Paracetamol',
            'dosagem': 750,
            'unidade_medida': 'mg',
            'categoria': 'Antitérmicos'
        },
        {
            'nome': 'Loratadina',
            'principio_ativo': 'Loratadina',
            'dosagem': 10,
            'unidade_medida': 'mg',
            'categoria': 'Antialérgicos'
        },
    ]
    
    for med_data in medicamentos_data:
        categoria = CategoriaMedicamento.objects.get(nome=med_data['categoria'])
        medicamento, created = Medicamento.objects.get_or_create(
            nome=med_data['nome'],
            dosagem=med_data['dosagem'],
            unidade_medida=med_data['unidade_medida'],
            defaults={
                'principio_ativo': med_data['principio_ativo'],
                'categoria': categoria
            }
        )
        if created:
            print(f"✓ Medicamento {medicamento.nome_completo} criado")
    
    # Criar UBSs
    ubs_data = [
        {
            'nome': 'UBS Centro',
            'endereco': 'Rua das Flores, 123',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234-567',
            'telefone': '(11) 1234-5678',
            'email': 'centro@ubs.com.br',
            'responsavel': admin
        },
        {
            'nome': 'UBS Norte',
            'endereco': 'Av. Paulista, 456',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234-890',
            'telefone': '(11) 2345-6789',
            'email': 'norte@ubs.com.br',
            'responsavel': operador1
        },
        {
            'nome': 'UBS Sul',
            'endereco': 'Rua da Saúde, 789',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01234-123',
            'telefone': '(11) 3456-7890',
            'email': 'sul@ubs.com.br',
            'responsavel': admin
        },
    ]
    
    for ubs_data_item in ubs_data:
        ubs, created = UBS.objects.get_or_create(
            nome=ubs_data_item['nome'],
            defaults=ubs_data_item
        )
        if created:
            print(f"✓ UBS {ubs.nome} criada")
    
    # Criar lotes de medicamentos
    medicamentos = Medicamento.objects.all()
    ubs_list = UBS.objects.all()
    
    for ubs in ubs_list:
        for medicamento in medicamentos:
            # Criar lote com validade futura
            lote, created = LoteMedicamento.objects.get_or_create(
                medicamento=medicamento,
                ubs=ubs,
                numero_lote=f"LOTE-{medicamento.id}-{ubs.id}-001",
                defaults={
                    'data_validade': timezone.now().date() + timedelta(days=365),
                    'quantidade_inicial': 100,
                    'quantidade_atual': 100,
                    'preco_unitario': 5.50
                }
            )
            if created:
                print(f"✓ Lote {lote.numero_lote} criado para {medicamento.nome} na {ubs.nome}")
    
    # Criar configurações de estoque mínimo
    for ubs in ubs_list:
        for medicamento in medicamentos:
            estoque_min, created = EstoqueMinimo.objects.get_or_create(
                medicamento=medicamento,
                ubs=ubs,
                defaults={'quantidade_minima': 20}
            )
            if created:
                print(f"✓ Estoque mínimo configurado para {medicamento.nome} na {ubs.nome}")
    
    print("\n✅ Dados de exemplo criados com sucesso!")
    print("\nUsuários criados:")
    print("- admin / admin123 (Administrador)")
    print("- operador1 / operador123 (Operador)")
    print("\nAcesse o sistema em: http://localhost:8000/admin/")

if __name__ == '__main__':
    create_sample_data()

