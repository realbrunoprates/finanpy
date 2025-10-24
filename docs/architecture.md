# Arquitetura Técnica

Documentação sobre decisões técnicas, stack e arquitetura do Finanpy.

## Visão Geral

O Finanpy adota uma arquitetura monolítica tradicional do Django, priorizando simplicidade e facilidade de manutenção. A escolha tecnológica evita over-engineering e foca em entregar funcionalidades de forma eficiente.

## Stack Tecnológica

### Backend

**Python 3.13+**
- Linguagem principal do projeto
- Moderna, madura e com excelente suporte da comunidade
- Ótima para prototipagem rápida e MVP

**Django 5+**
- Framework web full-stack
- Batteries included: ORM, Admin, Auth, Forms, etc.
- Segurança robusta out-of-the-box
- Excelente documentação

### Frontend

**Django Template Language (DTL)**
- Engine de templates nativa do Django
- Simplicidade sem necessidade de framework JavaScript separado
- Renderização server-side
- Menos complexidade no build process

**TailwindCSS**
- Framework CSS utility-first
- Design moderno e responsivo
- Customização fácil de cores e espaçamentos
- Menor curva de aprendizado que frameworks de componentes

**Vanilla JavaScript**
- JavaScript mínimo, apenas quando necessário
- Sem frameworks pesados (React, Vue, etc.)
- Foco em progressive enhancement

### Banco de Dados

**SQLite3**
- Banco de dados padrão do Django
- Zero configuração
- Perfeito para MVP e desenvolvimento
- Arquivo único, fácil de versionar em desenvolvimento
- Migração futura para PostgreSQL planejada

### Autenticação

**Django Auth (nativo)**
- Sistema de autenticação padrão do Django
- Seguro, testado e amplamente utilizado
- Hash de senhas com PBKDF2
- Gerenciamento de sessões integrado

## Arquitetura de Dados

### Modelo de Dados

O sistema segue o padrão relacional clássico com as seguintes entidades:

```
User (Django built-in)
├── Profile (1:1)
├── Account (1:N)
└── Category (1:N)

Account (1:N) → Transaction
Category (1:N) → Transaction
```

### Relacionamentos

**User → Profile** (One-to-One)
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
```

**User → Account** (One-to-Many)
```python
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
```

**User → Category** (One-to-Many)
```python
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10)  # 'income' ou 'expense'
```

**Account → Transaction** (One-to-Many)
**Category → Transaction** (One-to-Many)
```python
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
```

### Isolamento de Dados

**Princípio**: Cada usuário só acessa seus próprios dados.

Implementado via:
- Foreign Keys para User em todos os modelos principais
- Filtros automáticos nas queries: `.filter(user=request.user)`
- Validações em views e forms
- Decorators `@login_required` em todas as views autenticadas

```python
# Sempre filtrar por usuário logado
accounts = Account.objects.filter(user=request.user)
transactions = Transaction.objects.filter(account__user=request.user)
```

## Padrão de Arquitetura

### MVT (Model-View-Template)

Django usa o padrão MVT, variação do MVC:

**Model**: Lógica de dados e regras de negócio
```python
class Account(models.Model):
    # Campos do modelo
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    # Métodos de negócio
    def update_balance(self, amount, transaction_type):
        if transaction_type == 'income':
            self.balance += amount
        else:
            self.balance -= amount
        self.save()
```

**View**: Lógica de controle e coordenação
```python
@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account.update_balance(transaction.amount, transaction.type)
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/form.html', {'form': form})
```

**Template**: Apresentação e interface
```html
{% extends 'base.html' %}
{% block content %}
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Salvar</button>
    </form>
{% endblock %}
```

### Separação de Responsabilidades

**Models**: Apenas dados e lógica de negócio relacionada aos dados
- Campos e validações
- Métodos de instância relacionados ao modelo
- Properties calculadas
- Signals quando necessário

**Views**: Coordenação e fluxo
- Autenticação e autorização
- Receber dados do request
- Chamar métodos dos models
- Preparar contexto para templates
- Retornar resposta

**Templates**: Apenas apresentação
- Exibir dados
- Estrutura HTML
- Estilos com TailwindCSS
- JavaScript mínimo para interatividade

**Forms**: Validação de entrada
- Validação de campos
- Limpeza de dados
- Mensagens de erro

## Fluxo de Dados

### Fluxo de Request

```
1. Usuário faz requisição HTTP
   ↓
2. Django URL Dispatcher (urls.py)
   ↓
3. Middleware (autenticação, sessão, etc.)
   ↓
4. View (lógica de controle)
   ↓
5. Model (acesso a dados)
   ↓
6. Template (renderização)
   ↓
7. Response HTTP
```

### Exemplo Prático: Criar Transação

```
POST /transactions/create/
   ↓
urls.py → create_transaction view
   ↓
@login_required verifica autenticação
   ↓
View valida form (TransactionForm)
   ↓
View cria instância Transaction
   ↓
Transaction.save() persiste no banco
   ↓
Account.update_balance() atualiza saldo
   ↓
Redirect para lista de transações
   ↓
Renderiza template com mensagem de sucesso
```

## Decisões Arquiteturais

### Por que SQLite?

**Vantagens**:
- Zero configuração necessária
- Arquivo único, fácil de gerenciar
- Perfeito para MVP e desenvolvimento
- Migração simples para PostgreSQL depois

**Limitações conhecidas**:
- Não ideal para múltiplos escritores simultâneos
- Limitações de escalabilidade
- Plano de migração para PostgreSQL no futuro

### Por que Django Templates?

**Vantagens**:
- Simplicidade: sem build tools complexos
- Server-side rendering: melhor SEO e performance inicial
- Menos JavaScript = menos complexidade
- Ideal para CRUD tradicional

**Trade-offs**:
- Menos interatividade que SPAs
- Full page reloads
- Aceitável para o escopo do MVP

### Por que TailwindCSS?

**Vantagens**:
- Utility-first: desenvolvimento rápido
- Customização fácil de design system
- Responsivo por padrão
- Menor bundle que frameworks de componentes

**Trade-offs**:
- Classes longas no HTML
- Requer build process (PostCSS)
- Aceitável pelo ganho em produtividade

## Segurança

### Autenticação e Autorização

**Implementado**:
- Django Auth para login/logout
- Hash de senhas com PBKDF2 (padrão Django)
- Proteção CSRF em formulários
- Session-based authentication

**Validações**:
```python
# Sempre em views autenticadas
@login_required
def view_function(request):
    # Verificar propriedade do recurso
    resource = get_object_or_404(Model, id=resource_id)
    if resource.user != request.user:
        return HttpResponseForbidden()
```

### Proteções Django Built-in

- **SQL Injection**: ORM previne automaticamente
- **XSS**: Templates escapam HTML por padrão
- **CSRF**: Token obrigatório em forms
- **Clickjacking**: X-Frame-Options habilitado

### Configurações de Produção (futuras)

Para produção, alterar em settings.py:
```python
DEBUG = False
ALLOWED_HOSTS = ['dominio.com']
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Escalabilidade

### Plano de Crescimento

**Fase 1 (Atual)**: MVP com SQLite
- Até ~100 usuários
- Servidor único
- Simples e funcional

**Fase 2**: PostgreSQL
- Migração do banco de dados
- Suporte a mais usuários simultâneos
- Melhor performance de queries

**Fase 3**: Caching
- Redis para cache de sessões
- Cache de queries frequentes
- Melhor performance geral

**Fase 4**: Separação de Serviços (se necessário)
- API REST (Django REST Framework)
- Frontend separado (React/Vue)
- Microsserviços para módulos específicos

### Otimizações Previstas

**Queries**:
- `select_related()` para Foreign Keys
- `prefetch_related()` para Many-to-Many
- Índices em campos frequentemente consultados

**Cache**:
- Cache de template fragments
- Cache de queries repetitivas
- Cache de saldo consolidado

**Static Files**:
- Servir via CDN em produção
- Minificação de CSS e JS
- Lazy loading de imagens

## Monitoramento (futuro)

### Métricas a Acompanhar

- Tempo de resposta das views
- Número de queries por request
- Erros e exceções
- Uso de memória e CPU
- Número de usuários ativos

### Ferramentas Sugeridas

- Django Debug Toolbar (desenvolvimento)
- Sentry (erros em produção)
- New Relic ou similar (performance)
- PostgreSQL logs (queries lentas)

## Testes (planejados)

### Estratégia de Testes

**Unit Tests**: Testar modelos e métodos isoladamente
```python
class AccountModelTest(TestCase):
    def test_update_balance_income(self):
        account = Account.objects.create(balance=1000)
        account.update_balance(500, 'income')
        self.assertEqual(account.balance, 1500)
```

**Integration Tests**: Testar views e fluxos completos
```python
class TransactionViewTest(TestCase):
    def test_create_transaction(self):
        response = self.client.post('/transactions/create/', {
            'amount': 100,
            'type': 'income'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.count(), 1)
```

## Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
