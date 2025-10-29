# Setup e Instalação

Guia para configurar o ambiente de desenvolvimento do Finanpy.

## Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)
- Git

## Instalação

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd finanpy
```

### 2. Crie o Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

## Configuração

### 1. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste os valores conforme o ambiente:

```bash
cp .env.example .env
```

Variáveis principais:

- `SECRET_KEY`: chave secreta obrigatória do Django.
- `DEBUG`: mantenha `True` apenas em desenvolvimento.
- `ENVIRONMENT`: use `development` ou `production`. Quando definido como `production`, os padrões de segurança ficam mais rígidos.
- `SECURE_SSL_REDIRECT`: habilite (`True`) para forçar HTTPS.
- `SESSION_COOKIE_SECURE` e `CSRF_COOKIE_SECURE`: marcam os cookies como seguros (HTTPS apenas).
- `SECURE_HSTS_SECONDS`: define a duração da política HSTS (ex.: `31536000` para 1 ano, `0` para desativar).

> Para produção, defina `ENVIRONMENT=production`, `DEBUG=False` e ative todas as flags de segurança.

### 2. Banco de Dados

Execute as migrações para criar as tabelas no banco de dados SQLite:

```bash
python manage.py migrate
```

### 3. Crie um Superusuário

Para acessar o admin do Django:

```bash
python manage.py createsuperuser
```

## Executando o Projeto

### Servidor de Desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000/`

### Admin do Django

Acesse o painel administrativo em: `http://127.0.0.1:8000/admin/`

## Estrutura de Arquivos Importantes

```
finanpy/
├── manage.py              # Script de gerenciamento Django
├── requirements.txt       # Dependências Python
├── db.sqlite3            # Banco de dados SQLite
├── core/                 # Configurações do projeto Django
│   ├── settings.py       # Configurações principais
│   ├── urls.py          # URLs principais
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
├── users/               # App de usuários
├── profiles/            # App de perfis
├── accounts/            # App de contas bancárias
├── categories/          # App de categorias
└── transactions/        # App de transações
```

## Comandos Úteis

### Criar Migrações

```bash
python manage.py makemigrations
```

### Aplicar Migrações

```bash
python manage.py migrate
```

### Criar App Django

```bash
python manage.py startapp nome_do_app
```

### Shell Interativo

```bash
python manage.py shell
```

### Verificar Projeto

```bash
python manage.py check
```

## Troubleshooting

### Erro de Importação

Se encontrar erros de importação, certifique-se de que o ambiente virtual está ativado:
```bash
which python  # deve apontar para venv/bin/python
```

### Erro de Banco de Dados

Se houver problemas com o banco de dados, você pode recriá-lo:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Porta em Uso

Se a porta 8000 estiver ocupada, você pode usar outra:
```bash
python manage.py runserver 8080
```

## Próximos Passos

Após a instalação, consulte:
- [Estrutura do Projeto](project-structure.md) para entender a organização
- [Padrões de Código](coding-standards.md) para convenções de desenvolvimento
- [Arquitetura](architecture.md) para decisões técnicas
