# Estrutura do Projeto

Documentação sobre a organização de pastas e apps do Finanpy.

## Visão Geral

O Finanpy segue a estrutura padrão do Django, organizado em apps com responsabilidades bem definidas. Cada app é responsável por uma área específica do sistema.

## Estrutura de Diretórios

```
finanpy/
├── core/                    # Configurações principais do Django
├── users/                   # Gerenciamento de usuários
├── profiles/                # Perfis de usuários
├── accounts/                # Contas bancárias
├── categories/              # Categorias de transações
├── transactions/            # Transações financeiras
├── docs/                    # Documentação do projeto
├── venv/                    # Ambiente virtual Python
├── manage.py                # Script de gerenciamento Django
├── requirements.txt         # Dependências Python
├── db.sqlite3              # Banco de dados SQLite
├── PRD.md                  # Product Requirements Document
└── .gitignore              # Arquivos ignorados pelo Git
```

## Apps Django

O projeto está organizado em 5 apps principais:

### 1. core/

**Responsabilidade**: Configurações globais do projeto Django.

**Conteúdo**:
- `settings.py` - Configurações do Django (apps instalados, banco de dados, etc.)
- `urls.py` - URLs principais do projeto
- `wsgi.py` - Configuração WSGI para produção
- `asgi.py` - Configuração ASGI para aplicações assíncronas

**Status**: Configurado e funcional

### 2. users/

**Responsabilidade**: Extensão do modelo de usuário padrão do Django.

**Funcionalidades planejadas**:
- Autenticação de usuários (login/logout)
- Cadastro de novos usuários
- Gerenciamento de sessões

**Estrutura**:
```
users/
├── __init__.py
├── admin.py           # Configuração do admin
├── apps.py            # Configuração do app
├── models.py          # Modelos de dados
├── views.py           # Views e lógica de negócio
├── tests.py           # Testes unitários
└── migrations/        # Migrações do banco de dados
```

**Status**: Estrutura criada, modelos não implementados

### 3. profiles/

**Responsabilidade**: Perfis de usuários com informações adicionais.

**Funcionalidades planejadas**:
- Perfil criado automaticamente ao cadastrar usuário
- Nome completo, telefone e outras informações pessoais
- Visualização e edição de perfil

**Estrutura**:
```
profiles/
├── __init__.py
├── admin.py           # Configuração do admin
├── apps.py            # Configuração do app
├── models.py          # Modelo Profile
├── views.py           # Views de perfil
├── tests.py           # Testes unitários
└── migrations/        # Migrações do banco de dados
```

**Relacionamento**: Profile 1:1 com User

**Status**: Estrutura criada, modelos não implementados

### 4. accounts/

**Responsabilidade**: Gerenciamento de contas bancárias do usuário.

**Funcionalidades planejadas**:
- Cadastro de múltiplas contas bancárias
- Tipos: conta corrente, poupança, carteira
- Controle de saldo por conta
- Listagem, edição e exclusão de contas

**Estrutura**:
```
accounts/
├── __init__.py
├── admin.py           # Configuração do admin
├── apps.py            # Configuração do app
├── models.py          # Modelo Account
├── views.py           # Views CRUD de contas
├── tests.py           # Testes unitários
└── migrations/        # Migrações do banco de dados
```

**Relacionamento**: Account N:1 com User

**Status**: Estrutura criada, modelos não implementados

### 5. categories/

**Responsabilidade**: Categorias para classificação de transações.

**Funcionalidades planejadas**:
- Criação de categorias personalizadas
- Tipos: entrada ou saída
- Cores para identificação visual
- CRUD completo de categorias

**Estrutura**:
```
categories/
├── __init__.py
├── admin.py           # Configuração do admin
├── apps.py            # Configuração do app
├── models.py          # Modelo Category
├── views.py           # Views CRUD de categorias
├── tests.py           # Testes unitários
└── migrations/        # Migrações do banco de dados
```

**Relacionamento**: Category N:1 com User

**Status**: Estrutura criada, modelos não implementados

### 6. transactions/

**Responsabilidade**: Registro e controle de transações financeiras.

**Funcionalidades planejadas**:
- Registro de entradas e saídas
- Associação com conta e categoria
- Filtros por período, conta e categoria
- Atualização automática de saldos
- CRUD completo de transações

**Estrutura**:
```
transactions/
├── __init__.py
├── admin.py           # Configuração do admin
├── apps.py            # Configuração do app
├── models.py          # Modelo Transaction
├── views.py           # Views CRUD de transações
├── tests.py           # Testes unitários
└── migrations/        # Migrações do banco de dados
```

**Relacionamentos**:
- Transaction N:1 com Account
- Transaction N:1 com Category

**Status**: Estrutura criada, modelos não implementados

## Estrutura Padrão de um App Django

Cada app no Finanpy segue a estrutura padrão:

```
nome_do_app/
├── __init__.py          # Define o diretório como package Python
├── admin.py             # Registro de modelos no Django Admin
├── apps.py              # Configuração do app
├── models.py            # Definição dos modelos (tabelas do banco)
├── views.py             # Lógica de negócio e views
├── tests.py             # Testes unitários e de integração
├── migrations/          # Histórico de migrações do banco de dados
│   └── __init__.py
└── __pycache__/         # Cache Python (não versionado)
```

### Arquivos Adicionais (quando necessário)

Conforme o desenvolvimento, apps podem incluir:

```
nome_do_app/
├── urls.py              # URLs específicas do app
├── forms.py             # Formulários Django
├── serializers.py       # Serializers (se usar API)
├── signals.py           # Signals para ações automáticas
├── managers.py          # Custom managers para queries
├── templatetags/        # Tags customizadas para templates
└── templates/           # Templates HTML do app
    └── nome_do_app/
```

## Princípios de Organização

### Separação de Responsabilidades

Cada app tem uma responsabilidade única e bem definida:
- **users**: Apenas autenticação e modelo de usuário
- **profiles**: Apenas dados extras do perfil
- **accounts**: Apenas contas bancárias
- **categories**: Apenas categorias
- **transactions**: Apenas transações

### Coesão e Acoplamento

- Apps são coesos (alta coesão interna)
- Apps têm baixo acoplamento entre si
- Relacionamentos via Foreign Keys nos modelos
- Importações entre apps devem ser minimizadas

### Escalabilidade

A estrutura permite:
- Adicionar novos apps facilmente
- Mover apps para microsserviços futuramente
- Testar apps de forma independente
- Reutilizar apps em outros projetos

## Convenções de Nomenclatura

### Nomes de Apps
- Plural (accounts, categories, transactions)
- Minúsculas
- Uma palavra quando possível
- Descritivos da responsabilidade

### Nomes de Arquivos
- Minúsculas com underscores (snake_case)
- Seguir convenções Django (models.py, views.py, etc.)

### Nomes de Diretórios
- Minúsculas
- Sem espaços ou caracteres especiais

## Próximos Passos

Para entender melhor o projeto, consulte:
- [Padrões de Código](coding-standards.md) - Convenções de desenvolvimento
- [Arquitetura](architecture.md) - Decisões técnicas e fluxo de dados
