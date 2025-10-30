# Checklist de Deploy

Guia rápido para preparar e validar um deploy do Finanpy em produção.

## Pré-Deploy

- Confirmar branch principal atualizada e testes da pipeline passando.
- Rodar `python manage.py test` e verificar que todos os testes passam localmente.
- Executar `python manage.py tailwind build` para gerar CSS final.
- Rodar `python manage.py collectstatic --noinput` após o build do Tailwind.

## Configuração do Ambiente

- Definir variáveis de ambiente essenciais:
  - `ENVIRONMENT=production`
  - `DEBUG=False`
  - `SECRET_KEY` com valor seguro
  - `ALLOWED_HOSTS` com domínios e/ou IPs da aplicação
  - `DATABASE_URL` do banco de dados de produção
  - `DB_CONN_MAX_AGE` (ex.: `600`) e `DB_SSL_REQUIRE=True` quando o provedor exigir TLS
  - Flags de segurança: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`
- Instalar dependências de produção com `pip install -r requirements/production.txt`.

## Banco de Dados e Arquivos

- Aplicar migrações com `python manage.py migrate`.
- Criar superusuário (caso ainda não exista) com `python manage.py createsuperuser`.
- Garantir acesso ao armazenamento de estáticos (S3, disco ou equivalente).

## Validação Técnica

- Testar o servidor com `gunicorn core.wsgi:application` apontando para `ENVIRONMENT=production`.
- Verificar logs de inicialização buscando erros de banco, templates ou imports.
- Acessar a aplicação em ambiente de staging ou sandbox e validar login, dashboard e cadastros principais.

## Pós-Deploy

- Monitorar erros (Sentry, logs do provedor) durante as primeiras horas.
- Validar geração de novas transações e atualização de saldo.
- Atualizar documentação ou PR com qualquer ajuste extra executado.
