# Sistema de Signals - Transactions

## Visão Geral

O sistema de signals do app `transactions` garante que o saldo das contas seja **atualizado automaticamente** sempre que uma transação é criada, atualizada ou deletada.

Este é um componente **crítico** do sistema Finanpy, responsável por manter a **consistência dos dados financeiros**.

## Arquitetura

```
Transaction (save/delete)
    ↓
Django Signals (pre_save, post_save, post_delete)
    ↓
Balance Update Logic
    ↓
Account.balance (atualizado automaticamente)
```

## Signals Implementados

### 1. `pre_save` - Armazenar Estado Anterior

**Função**: `store_old_transaction_data()`

**Objetivo**: Armazena o estado anterior da transação antes de salvar, permitindo detectar mudanças.

**Quando executa**: Antes de `save()` em transações existentes (não em creates).

**O que armazena**:
- `_old_account`: Conta anterior
- `_old_amount`: Valor anterior
- `_old_transaction_type`: Tipo anterior (income/expense)

```python
# Exemplo interno do signal
instance._old_account = old_transaction.account
instance._old_amount = old_transaction.amount
instance._old_transaction_type = old_transaction.transaction_type
```

### 2. `post_save` - Atualizar Saldo

**Função**: `update_balance_on_save()`

**Objetivo**: Atualiza o saldo da conta após criar ou atualizar uma transação.

**Quando executa**: Após `save()` bem-sucedido.

**Cenários tratados**:

#### A) Create (nova transação)
```python
Transaction.objects.create(
    account=account,
    transaction_type='income',
    amount=Decimal('500.00'),
    ...
)
# Saldo da conta aumenta em R$ 500
```

#### B) Update - Mesmo conta, valor diferente
```python
transaction.amount = Decimal('800.00')  # Era 500
transaction.save()
# Reverte 500 e aplica 800 (diferença de +300)
```

#### C) Update - Mudança de tipo
```python
transaction.transaction_type = 'income'  # Era expense
transaction.save()
# Reverte expense (-200 vira +200) e aplica income (+200)
# Total: +400 no saldo
```

#### D) Update - Mudança de conta
```python
transaction.account = account2  # Era account1
transaction.save()
# Reverte na account1 e aplica na account2
```

### 3. `post_delete` - Reverter Saldo

**Função**: `update_balance_on_delete()`

**Objetivo**: Reverte o impacto da transação deletada no saldo da conta.

**Quando executa**: Após `delete()` bem-sucedido.

```python
transaction.delete()
# Se era INCOME: saldo diminui
# Se era EXPENSE: saldo aumenta
```

## Função Auxiliar

### `_update_account_balance()`

Função privada que executa a lógica de atualização do saldo.

**Parâmetros**:
- `account`: Instância do Account
- `amount`: Valor da transação (Decimal)
- `transaction_type`: 'income' ou 'expense'
- `operation`: 'add' ou 'remove'

**Lógica**:

| Tipo | Operação | Efeito no Saldo |
|------|----------|-----------------|
| INCOME | add | +valor |
| INCOME | remove | -valor |
| EXPENSE | add | -valor |
| EXPENSE | remove | +valor |

**Recursos de segurança**:
- `account.refresh_from_db()`: Garante dados atualizados
- `transaction.atomic()`: Garante atomicidade
- `update_fields=['balance', 'updated_at']`: Evita loops infinitos

## Garantias de Consistência

### 1. Atomicidade
Usa `transaction.atomic()` para garantir que atualizações de saldo sejam atômicas:
```python
with transaction.atomic():
    # Operações no saldo aqui
    account.save(update_fields=['balance', 'updated_at'])
```

### 2. Refresh from Database
Sempre busca dados atualizados antes de atualizar:
```python
account.refresh_from_db()
account.balance += amount
account.save()
```

### 3. Update Fields Específicos
Evita loops infinitos de signals usando `update_fields`:
```python
account.save(update_fields=['balance', 'updated_at'])
```

## Limitações Conhecidas

### Bulk Operations
**Signals NÃO são disparados** em operações bulk do Django:

```python
# ❌ NÃO dispara signals
Transaction.objects.bulk_create([...])
Transaction.objects.filter(...).update(amount=100)
Transaction.objects.filter(...).delete()

# ✅ Dispara signals
for data in transactions_data:
    Transaction.objects.create(**data)
```

**Solução**: Use loops com `.save()` e `.delete()` individuais quando precisar disparar signals.

## Testes

### Executar Testes Automatizados

```bash
# Teste rápido com validação de todos os cenários
python test_signals_quick.py
```

**Saída esperada**: Todos os testes com ✓ (checkmark verde)

### Testes Manuais via Shell

Consulte `SIGNALS_TEST.md` para guia detalhado de testes manuais via Django shell.

```bash
python manage.py shell
# Seguir instruções em SIGNALS_TEST.md
```

## Troubleshooting

### Problema: Saldo não atualiza

**Diagnóstico**:
1. Verificar se signals estão registrados:
```bash
python manage.py shell
>>> from django.db.models.signals import post_save
>>> from transactions.models import Transaction
>>> print(post_save._live_receivers(Transaction))
```

2. Verificar se apps.py tem método `ready()`:
```python
# transactions/apps.py
def ready(self):
    import transactions.signals
```

3. Reiniciar servidor Django após mudanças em signals.py

**Solução**: Se signals não estão registrados, verificar import em apps.py e reiniciar servidor.

### Problema: IntegrityError ou OperationalError

**Causa**: Concorrência ou transações aninhadas

**Solução**: Usar `transaction.atomic()` em views complexas:
```python
from django.db import transaction

@transaction.atomic
def my_view(request):
    # Operações aqui
```

### Problema: Recursão infinita

**Causa**: Signal disparando outro save() sem `update_fields`

**Solução**: Sempre usar `update_fields` em saves dentro de signals:
```python
account.save(update_fields=['balance', 'updated_at'])
```

## Manutenção

### Adicionar Novo Campo que Afeta Saldo

1. Atualizar `_update_account_balance()` com nova lógica
2. Atualizar `store_old_transaction_data()` para armazenar campo antigo
3. Atualizar `update_balance_on_save()` para comparar mudanças
4. Adicionar testes em `test_signals_quick.py`

### Logs e Monitoramento

Em produção, substitua `print()` por logging adequado:

```python
import logging

logger = logging.getLogger(__name__)

except Exception as e:
    logger.error(f'Erro ao atualizar saldo: {str(e)}', exc_info=True)
    raise
```

## Referências

- [Django Signals Documentation](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Django Database Transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/)
- `docs/architecture.md` - Decisões arquiteturais do projeto
- `PRD.md` - Requisitos de negócio

## Checklist de Validação

Antes de fazer commit de mudanças em signals:

- [ ] Todos os cenários testados (create, update, delete)
- [ ] Mudanças de conta testadas
- [ ] Mudanças de tipo testadas
- [ ] Mudanças de valor testadas
- [ ] Atomicidade garantida com `transaction.atomic()`
- [ ] `update_fields` usado para evitar loops
- [ ] `refresh_from_db()` usado antes de atualizar saldo
- [ ] Tratamento de erros implementado
- [ ] Testes automatizados passando
- [ ] Sem regressões em funcionalidades existentes
