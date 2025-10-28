# Guia de Testes Manuais - Transaction Signals

Este documento descreve como testar manualmente o sistema de signals de transações via Django shell.

## Setup Inicial

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Abrir Django shell
python manage.py shell
```

## Criar Dados de Teste

```python
from django.contrib.auth import get_user_model
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from decimal import Decimal

User = get_user_model()

# Criar ou buscar usuário de teste
user = User.objects.first()  # Ou criar um novo

# Criar conta de teste
account = Account.objects.create(
    user=user,
    name='Conta Teste Signals',
    bank_name='Banco Teste',
    account_type='checking',
    balance=Decimal('1000.00')
)

print(f'Saldo inicial da conta: R$ {account.balance}')

# Criar categorias de teste
income_category = Category.objects.create(
    user=user,
    name='Salário',
    category_type='income'
)

expense_category = Category.objects.create(
    user=user,
    name='Alimentação',
    category_type='expense'
)
```

## Teste 1: Criar Transação de INCOME

```python
# Criar transação de entrada (receita)
from datetime import date

transaction1 = Transaction.objects.create(
    account=account,
    category=income_category,
    transaction_type='income',
    amount=Decimal('500.00'),
    transaction_date=date.today(),
    description='Teste de receita'
)

# Verificar saldo atualizado
account.refresh_from_db()
print(f'Saldo após INCOME de R$ 500: R$ {account.balance}')
# Esperado: R$ 1500.00 (1000 + 500)
```

## Teste 2: Criar Transação de EXPENSE

```python
# Criar transação de saída (despesa)
transaction2 = Transaction.objects.create(
    account=account,
    category=expense_category,
    transaction_type='expense',
    amount=Decimal('200.00'),
    transaction_date=date.today(),
    description='Teste de despesa'
)

# Verificar saldo atualizado
account.refresh_from_db()
print(f'Saldo após EXPENSE de R$ 200: R$ {account.balance}')
# Esperado: R$ 1300.00 (1500 - 200)
```

## Teste 3: Atualizar Valor da Transação

```python
# Atualizar valor da transação1 (INCOME)
print(f'Saldo antes da atualização: R$ {account.balance}')  # 1300

transaction1.amount = Decimal('800.00')  # Era 500, agora 800
transaction1.save()

account.refresh_from_db()
print(f'Saldo após atualizar INCOME de 500 para 800: R$ {account.balance}')
# Esperado: R$ 1600.00 (1300 - 500 + 800)
```

## Teste 4: Alterar Tipo da Transação

```python
# Alterar tipo de EXPENSE para INCOME
print(f'Saldo antes de mudar tipo: R$ {account.balance}')  # 1600

transaction2.transaction_type = 'income'  # Era expense, agora income
transaction2.save()

account.refresh_from_db()
print(f'Saldo após mudar EXPENSE para INCOME (R$ 200): R$ {account.balance}')
# Esperado: R$ 2000.00 (1600 + 200 + 200)
# Explicação: remove o impacto da expense (-200 se torna +200) e adiciona como income (+200)
```

## Teste 5: Mudar Conta da Transação

```python
# Criar segunda conta
account2 = Account.objects.create(
    user=user,
    name='Conta Teste 2',
    bank_name='Banco Teste 2',
    account_type='savings',
    balance=Decimal('500.00')
)

print(f'Saldo conta 1 antes: R$ {account.balance}')    # 2000
print(f'Saldo conta 2 antes: R$ {account2.balance}')   # 500

# Mover transaction1 (INCOME de 800) da account para account2
transaction1.account = account2
transaction1.save()

account.refresh_from_db()
account2.refresh_from_db()

print(f'Saldo conta 1 depois: R$ {account.balance}')   # Esperado: 1200 (2000 - 800)
print(f'Saldo conta 2 depois: R$ {account2.balance}')  # Esperado: 1300 (500 + 800)
```

## Teste 6: Deletar Transação

```python
print(f'Saldo conta 2 antes de deletar: R$ {account2.balance}')  # 1300

# Deletar transaction1 (INCOME de 800)
transaction1.delete()

account2.refresh_from_db()
print(f'Saldo conta 2 após deletar INCOME de 800: R$ {account2.balance}')
# Esperado: R$ 500.00 (1300 - 800)
```

## Teste 7: Múltiplas Transações Simultâneas

```python
# Criar várias transações de uma vez
transactions = [
    Transaction(
        account=account,
        category=income_category,
        transaction_type='income',
        amount=Decimal('100.00'),
        transaction_date=date.today(),
        description=f'Receita {i}'
    ) for i in range(5)
]

print(f'Saldo antes de criar 5 transações de R$ 100: R$ {account.balance}')  # 1200

Transaction.objects.bulk_create(transactions)

# ATENÇÃO: bulk_create NÃO dispara signals!
# Para disparar signals, use save() individual

account.refresh_from_db()
print(f'Saldo após bulk_create: R$ {account.balance}')  # Ainda 1200 (signals não disparados)

# Criar com save() individual
for i in range(5):
    Transaction.objects.create(
        account=account,
        category=income_category,
        transaction_type='income',
        amount=Decimal('100.00'),
        transaction_date=date.today(),
        description=f'Receita save() {i}'
    )

account.refresh_from_db()
print(f'Saldo após 5 creates com save(): R$ {account.balance}')  # 1700 (1200 + 500)
```

## Limpeza

```python
# Deletar dados de teste
Transaction.objects.filter(account__in=[account, account2]).delete()
account.delete()
account2.delete()
income_category.delete()
expense_category.delete()
```

## Checklist de Validação

- [ ] Transação INCOME aumenta saldo da conta
- [ ] Transação EXPENSE diminui saldo da conta
- [ ] Atualizar valor recalcula saldo corretamente
- [ ] Mudar tipo (INCOME↔EXPENSE) ajusta saldo
- [ ] Mudar conta transfere saldo entre contas
- [ ] Deletar transação reverte o saldo
- [ ] Múltiplas operações mantém consistência
- [ ] Não há erros de concorrência ou loops infinitos
- [ ] balance é atualizado com transaction.atomic()

## Troubleshooting

### Saldos não batem?

1. Verificar se signals estão registrados:
```python
from django.db.models.signals import post_save
print(post_save.receivers)  # Deve conter receivers de Transaction
```

2. Verificar se apps.py tem ready():
```python
from transactions.apps import TransactionsConfig
print(hasattr(TransactionsConfig, 'ready'))  # Deve ser True
```

3. Reiniciar shell Django após mudanças em signals.py

### Erro de recursão infinita?

- Verificar se está usando `update_fields` no save() dentro dos signals
- Conferir se não há signals adicionais disparando em cascata

### Transações criadas via admin não atualizam saldo?

- Signals devem funcionar no admin também
- Verificar se há erros silenciosos no console do servidor
