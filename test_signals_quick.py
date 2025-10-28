#!/usr/bin/env python
"""
Script de teste rápido para validar signals de transações.

Execute com: python test_signals_quick.py
"""

import os
import django
from decimal import Decimal
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction

User = get_user_model()


def run_signal_tests():
    """Executa bateria de testes dos signals."""

    print('\n' + '=' * 80)
    print('TESTE DE SIGNALS - TRANSACTIONS')
    print('=' * 80 + '\n')

    # Setup
    user = User.objects.first()
    if not user:
        print('ERRO: Nenhum usuário encontrado. Crie um superuser primeiro.')
        return

    print(f'Usuário de teste: {user.email}\n')

    # Criar conta de teste
    account = Account.objects.create(
        user=user,
        name='Conta Teste Signals',
        bank_name='Banco Teste',
        account_type='checking',
        balance=Decimal('1000.00')
    )

    print(f'✓ Conta criada: {account.name}')
    print(f'  Saldo inicial: R$ {account.balance}\n')

    # Criar categorias
    income_cat, created = Category.objects.get_or_create(
        user=user,
        name='Teste Income Signals',
        defaults={'category_type': 'income'}
    )

    expense_cat, created = Category.objects.get_or_create(
        user=user,
        name='Teste Expense Signals',
        defaults={'category_type': 'expense'}
    )

    print('✓ Categorias criadas ou recuperadas\n')

    # TESTE 1: Criar INCOME
    print('-' * 80)
    print('TESTE 1: Criar transação INCOME')
    print('-' * 80)

    t1 = Transaction.objects.create(
        account=account,
        category=income_cat,
        transaction_type='income',
        amount=Decimal('500.00'),
        transaction_date=date.today(),
        description='Receita teste'
    )

    account.refresh_from_db()
    expected = Decimal('1500.00')
    status = '✓' if account.balance == expected else '✗'
    print(f'{status} INCOME de R$ 500.00')
    print(f'  Saldo esperado: R$ {expected}')
    print(f'  Saldo atual: R$ {account.balance}')
    print()

    # TESTE 2: Criar EXPENSE
    print('-' * 80)
    print('TESTE 2: Criar transação EXPENSE')
    print('-' * 80)

    t2 = Transaction.objects.create(
        account=account,
        category=expense_cat,
        transaction_type='expense',
        amount=Decimal('200.00'),
        transaction_date=date.today(),
        description='Despesa teste'
    )

    account.refresh_from_db()
    expected = Decimal('1300.00')
    status = '✓' if account.balance == expected else '✗'
    print(f'{status} EXPENSE de R$ 200.00')
    print(f'  Saldo esperado: R$ {expected}')
    print(f'  Saldo atual: R$ {account.balance}')
    print()

    # TESTE 3: Atualizar valor
    print('-' * 80)
    print('TESTE 3: Atualizar valor da transação')
    print('-' * 80)

    t1.amount = Decimal('800.00')
    t1.save()

    account.refresh_from_db()
    expected = Decimal('1600.00')
    status = '✓' if account.balance == expected else '✗'
    print(f'{status} Atualizar INCOME de R$ 500 para R$ 800')
    print(f'  Saldo esperado: R$ {expected}')
    print(f'  Saldo atual: R$ {account.balance}')
    print()

    # TESTE 4: Mudar tipo
    print('-' * 80)
    print('TESTE 4: Mudar tipo da transação')
    print('-' * 80)

    t2.transaction_type = 'income'
    t2.save()

    account.refresh_from_db()
    expected = Decimal('2000.00')
    status = '✓' if account.balance == expected else '✗'
    print(f'{status} Mudar de EXPENSE para INCOME (R$ 200)')
    print(f'  Saldo esperado: R$ {expected}')
    print(f'  Saldo atual: R$ {account.balance}')
    print()

    # TESTE 5: Deletar transação
    print('-' * 80)
    print('TESTE 5: Deletar transação')
    print('-' * 80)

    t1.delete()

    account.refresh_from_db()
    expected = Decimal('1200.00')
    status = '✓' if account.balance == expected else '✗'
    print(f'{status} Deletar INCOME de R$ 800')
    print(f'  Saldo esperado: R$ {expected}')
    print(f'  Saldo atual: R$ {account.balance}')
    print()

    # Limpeza
    print('-' * 80)
    print('LIMPEZA')
    print('-' * 80)

    Transaction.objects.filter(account=account).delete()
    account.delete()
    income_cat.delete()
    expense_cat.delete()

    print('✓ Dados de teste removidos')
    print('\n' + '=' * 80)
    print('TESTES CONCLUÍDOS')
    print('=' * 80 + '\n')


if __name__ == '__main__':
    run_signal_tests()
