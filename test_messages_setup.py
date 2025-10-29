"""
Script para preparar ambiente de teste de mensagens.
Cria usuários de teste e dados iniciais.
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

from accounts.models import Account
from categories.models import Category

User = get_user_model()

# Criar usuário de teste se não existir
email = 'qa.tester@finanpy.com'
password = 'TestPass123!'

try:
    user = User.objects.get(email=email)
    print(f'Usuário {email} já existe')
except User.DoesNotExist:
    user = User.objects.create_user(
        username='qa_tester',
        email=email,
        password=password,
        first_name='QA',
        last_name='Tester'
    )
    print(f'Usuário criado: {email}')

# Criar conta de teste se não existir
if not Account.objects.filter(user=user).exists():
    Account.objects.create(
        user=user,
        name='Conta Corrente Teste',
        account_type='checking',
        balance=1000.00
    )
    print('Conta de teste criada')

# Criar categorias de teste se não existir
if not Category.objects.filter(user=user, category_type=Category.INCOME).exists():
    Category.objects.create(
        user=user,
        name='Salário',
        category_type=Category.INCOME
    )
    print('Categoria de receita criada')

if not Category.objects.filter(user=user, category_type=Category.EXPENSE).exists():
    Category.objects.create(
        user=user,
        name='Alimentação',
        category_type=Category.EXPENSE
    )
    print('Categoria de despesa criada')

print('\nDados de teste:')
print(f'Email: {email}')
print(f'Senha: {password}')
print('Ambiente de teste preparado com sucesso!')
