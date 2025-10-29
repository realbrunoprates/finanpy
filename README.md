# Finanpy

Sistema de gestão financeira pessoal desenvolvido com Django 5+ e Python 3.13+.

## Sobre o Projeto

Finanpy é uma aplicação web para gerenciamento de finanças pessoais que permite aos usuários:

- Gerenciar contas bancárias (corrente, poupança, carteira)
- Criar e organizar categorias de receitas e despesas
- Registrar transações financeiras
- Visualizar dashboard com estatísticas e gráficos
- Controlar saldo automaticamente

## Tecnologias

- **Backend**: Python 3.13+, Django 5+
- **Frontend**: Django Template Language, TailwindCSS
- **Banco de Dados**: SQLite3 (desenvolvimento)
- **Autenticação**: Django Auth nativo

## Estrutura do Projeto

```
finanpy/
├── core/               # Configurações do Django
├── users/              # Autenticação e usuários
├── profiles/           # Perfis de usuário
├── accounts/           # Contas bancárias
├── categories/         # Categorias de transações
├── transactions/       # Transações financeiras
├── templates/          # Templates HTML globais
├── static/             # Arquivos estáticos
├── theme/              # App do TailwindCSS
├── docs/               # Documentação
└── agents/             # Agentes de IA para desenvolvimento
```

## Setup do Ambiente

### Requisitos

- Python 3.13 ou superior
- Node.js (para TailwindCSS)
- Git

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd finanpy
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
# Crie o arquivo .env na raiz do projeto
cp .env.example .env

# Edite o .env com suas configurações
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
```
Consulte a seção [Variáveis de Ambiente](#variáveis-de-ambiente) para detalhes e recomendações.

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Instale as dependências do TailwindCSS:
```bash
python manage.py tailwind install
```

## Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para separar credenciais e configurações sensíveis. As variáveis obrigatórias são:

- `SECRET_KEY`: chave criptográfica do Django. Gere um valor único para cada ambiente (use `django.core.management.utils.get_random_secret_key()` no shell).
- `DEBUG`: controla o modo debug (`True` apenas em desenvolvimento; defina `False` para produção).

Para ambientes de produção, configure também `ALLOWED_HOSTS` diretamente em `core/settings.py` ou adapte o código para lê-lo do `.env` conforme necessário.

## Executando o Projeto

### Modo Desenvolvimento

Em um terminal, inicie o servidor Django:
```bash
python manage.py runserver
```

Em outro terminal, inicie o TailwindCSS em modo watch:
```bash
python manage.py tailwind start
```

Acesse: `http://localhost:8000`

### Build de Produção

Para gerar o CSS minificado para produção:
```bash
python manage.py tailwind build
python manage.py collectstatic
```

## Comandos Úteis

```bash
# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Acessar shell do Django
python manage.py shell

# Verificar problemas
python manage.py check

# Criar superusuário
python manage.py createsuperuser
```

## Documentação

A documentação completa do projeto está disponível em:

- **docs/README.md** - Índice da documentação
- **docs/setup.md** - Guia de instalação e configuração
- **docs/project-structure.md** - Estrutura de apps e diretórios
- **docs/coding-standards.md** - Padrões de código
- **docs/architecture.md** - Arquitetura técnica
- **docs/design-system.md** - Sistema de design e componentes UI

Consulte também:
- **PRD.md** - Product Requirements Document
- **CLAUDE.md** - Guia para desenvolvimento com IA
- **TASKS.md** - Lista de tarefas organizadas por sprint

## Desenvolvimento com IA

O projeto inclui agentes de IA especializados em `agents/`:

- **backend-developer.md** - Desenvolvimento backend (Django, Python)
- **frontend-developer.md** - Desenvolvimento frontend (Templates, TailwindCSS)
- **qa-tester.md** - Testes e validação
- **tech-lead.md** - Arquitetura e code review

Consulte `agents/README.md` para mais informações.

## Padrões de Código

- **Linguagem**: Código em inglês, mensagens em português
- **Aspas**: Sempre use aspas simples (`'`)
- **Estilo Python**: Siga PEP 8
- **Commits**: Mensagens em português no infinitivo

## Licença

Este projeto é de uso pessoal e educacional.

## Autor

Bruno Prates
