# Padrões de Código

Convenções e boas práticas de desenvolvimento do Finanpy.

## Princípios Gerais

- **Simplicidade**: Evite over-engineering, mantenha o código simples e direto
- **Legibilidade**: Código deve ser fácil de ler e entender
- **Consistência**: Siga sempre os mesmos padrões em todo o projeto
- **Manutenibilidade**: Escreva código pensando em quem vai manter depois

## Python e Django

### PEP 8

Todo código Python deve seguir rigorosamente o [PEP 8](https://peps.python.org/pep-0008/).

**Principais pontos**:

```python
# Indentação: 4 espaços
def minha_funcao():
    if condicao:
        fazer_algo()

# Linhas: máximo 79 caracteres para código
# Máximo 72 caracteres para docstrings e comentários

# Imports: sempre no topo, organizados
# 1. Bibliotecas padrão
# 2. Bibliotecas de terceiros
# 3. Imports locais
import os
import sys

from django.db import models
from django.contrib.auth.models import User

from accounts.models import Account
```

### Aspas

**IMPORTANTE**: Use sempre aspas simples (`'`) ao invés de aspas duplas (`"`).

```python
# Correto
nome = 'Bruno'
mensagem = 'Bem-vindo ao Finanpy'

# Incorreto
nome = "Bruno"
mensagem = "Bem-vindo ao Finanpy"

# Exceção: strings com aspas simples internas
frase = "O usuário disse: 'olá'"
```

### Idioma

**Código em Inglês, Mensagens em Português**.

```python
# Correto: variáveis, funções e classes em inglês
class Account(models.Model):
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total(self):
        return self.balance

# Correto: mensagens para usuário em português
def criar_conta(request):
    messages.success(request, 'Conta criada com sucesso!')

# Incorreto: código em português
class Conta(models.Model):
    nome_conta = models.CharField(max_length=100)
```

### Nomes de Variáveis e Funções

**snake_case** para variáveis e funções:

```python
# Correto
user_profile = get_user_profile()
total_balance = calculate_total_balance()
is_active = True

# Incorreto
userProfile = getUserProfile()
TotalBalance = CalculateTotalBalance()
IsActive = True
```

### Nomes de Classes

**PascalCase** para classes:

```python
# Correto
class UserProfile(models.Model):
    pass

class AccountManager:
    pass

# Incorreto
class user_profile(models.Model):
    pass

class account_manager:
    pass
```

### Nomes de Constantes

**UPPER_CASE** para constantes:

```python
# Correto
MAX_UPLOAD_SIZE = 5242880
DEFAULT_CURRENCY = 'BRL'
ACCOUNT_TYPES = ['checking', 'savings', 'wallet']

# Incorreto
max_upload_size = 5242880
defaultCurrency = 'BRL'
```

## Modelos Django

### Campos Obrigatórios

Todo modelo deve ter:
- `created_at` - Data de criação
- `updated_at` - Data de atualização

```python
from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    # Campos obrigatórios em todos os modelos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

### Meta Class

Sempre defina `Meta` quando apropriado:

```python
class Transaction(models.Model):
    # ... campos

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
```

### Método __str__

Todo modelo deve ter um método `__str__` descritivo:

```python
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

### Related Names

Sempre defina `related_name` em Foreign Keys:

```python
class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'  # Sempre definir
    )
```

## Views

### Function-Based Views

Preferir function-based views quando a lógica é simples:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/list.html', {
        'accounts': accounts
    })
```

### Class-Based Views

Usar quando houver reutilização de código:

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
```

## Templates

### Nomenclatura

```
app_name/
└── templates/
    └── app_name/
        ├── base.html
        ├── list.html
        ├── detail.html
        ├── form.html
        └── partials/
            └── _card.html
```

### Django Template Language

```html
{% extends 'base.html' %}

{% block title %}Lista de Contas{% endblock %}

{% block content %}
<div class="container">
    {% for account in accounts %}
        <div class="card">
            <h3>{{ account.name }}</h3>
            <p>{{ account.balance|floatformat:2 }}</p>
        </div>
    {% empty %}
        <p>Nenhuma conta cadastrada.</p>
    {% endfor %}
</div>
{% endblock %}
```

## Formatação

### Imports

Organizar imports em grupos separados por linha em branco:

```python
# 1. Bibliotecas padrão Python
import os
import sys
from datetime import datetime

# 2. Bibliotecas Django
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# 3. Bibliotecas de terceiros
# (quando houver)

# 4. Imports locais do projeto
from accounts.models import Account
from categories.models import Category
```

### Espaçamento

```python
# Duas linhas em branco antes de classes e funções top-level
class MyClass:
    pass


def my_function():
    pass


# Uma linha em branco entre métodos de classe
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass
```

### Comentários

```python
# Comentários em português explicando o porquê, não o quê
def calculate_balance(transactions):
    # Calcula saldo considerando entradas e saídas
    # Necessário para manter consistência com o saldo da conta
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    return income - expense
```

### Docstrings

Usar docstrings em português para funções e classes importantes:

```python
def process_transaction(transaction, account):
    """
    Processa uma transação e atualiza o saldo da conta.

    Args:
        transaction: Instância de Transaction
        account: Instância de Account

    Returns:
        bool: True se processada com sucesso

    Raises:
        ValueError: Se o saldo for insuficiente para saída
    """
    pass
```

## Git e Versionamento

### Mensagens de Commit

Em português, verbos no infinitivo:

```bash
# Correto
git commit -m "Adicionar modelo Account"
git commit -m "Corrigir cálculo de saldo"
git commit -m "Atualizar documentação de setup"

# Incorreto
git commit -m "Added Account model"
git commit -m "Fix balance calculation"
git commit -m "Adicionado modelo Account"  # particípio
```

### Branches

```bash
# Feature
git checkout -b feature/adicionar-categorias

# Bugfix
git checkout -b fix/corrigir-saldo

# Hotfix
git checkout -b hotfix/seguranca-login
```

## Segurança

### Validação de Permissões

Sempre validar se o usuário tem permissão:

```python
@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    # Validar se a conta pertence ao usuário
    if account.user != request.user:
        return HttpResponseForbidden()

    # ... continuar processamento
```

### Sanitização de Inputs

Django faz automaticamente, mas sempre validar:

```python
from django import forms

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']

    def clean_balance(self):
        balance = self.cleaned_data['balance']
        if balance < 0:
            raise forms.ValidationError('Saldo não pode ser negativo')
        return balance
```

## Performance

### Queries Otimizadas

Usar `select_related` e `prefetch_related`:

```python
# Evitar N+1 queries
transactions = Transaction.objects.select_related(
    'account',
    'category'
).filter(account__user=request.user)
```

### Índices

Adicionar índices em campos frequentemente consultados:

```python
class Transaction(models.Model):
    transaction_date = models.DateField(db_index=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True)
```

## Testes

### Nomenclatura

```python
class AccountModelTest(TestCase):
    def test_create_account(self):
        pass

    def test_account_str_method(self):
        pass

    def test_calculate_balance(self):
        pass
```

### Organização

Um arquivo de teste por arquivo de código quando necessário:

```
accounts/
├── models.py
├── views.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_views.py
```

## Checklist de Code Review

Antes de fazer commit, verificar:

- [ ] Código segue PEP 8
- [ ] Aspas simples usadas consistentemente
- [ ] Código em inglês, mensagens em português
- [ ] Models têm `created_at` e `updated_at`
- [ ] Models têm `__str__` definido
- [ ] Foreign Keys têm `related_name`
- [ ] Imports organizados corretamente
- [ ] Validações de permissão implementadas
- [ ] Queries otimizadas quando necessário
- [ ] Código testado manualmente

## Ferramentas Recomendadas

### Linters

```bash
# Instalar flake8 para verificar PEP 8
pip install flake8

# Executar verificação
flake8 .
```

### Formatadores

```bash
# Instalar black para formatação automática
pip install black

# Formatar código
black .
```

## Referências

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- [Django Best Practices](https://docs.djangoproject.com/en/dev/misc/design-philosophies/)
