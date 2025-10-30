# Guia de Execução de Testes E2E - Finanpy

Este documento explica como executar os testes End-to-End (E2E) do fluxo de perfil usando Playwright.

---

## Pré-requisitos

### Software Necessário

1. **Python 3.12+** (já instalado)
2. **Virtualenv ativado** (venv)
3. **Playwright** e **Chromium** (instruções abaixo)
4. **Django** rodando (localhost:8000)

---

## Instalação do Playwright

Se ainda não tiver o Playwright instalado:

```bash
# Ativar virtualenv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar Playwright
pip install playwright

# Instalar navegador Chromium
playwright install chromium
```

---

## Configuração Inicial

### 1. Criar Usuário de Teste

Antes de executar os testes, crie o usuário de teste via Django shell:

```bash
source venv/bin/activate
python manage.py shell
```

Dentro do shell:

```python
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

# Deletar se já existir
User.objects.filter(email='teste_profile@finanpy.com').delete()

# Criar usuário de teste
user = User.objects.create_user(
    email='teste_profile@finanpy.com',
    password='TestPass123!@#'
)

print(f'User created: {user.email}')
print(f'Profile exists: {Profile.objects.filter(user=user).exists()}')
exit()
```

### 2. Iniciar Servidor Django

Em um terminal separado:

```bash
source venv/bin/activate
python manage.py runserver
```

Deixe o servidor rodando durante os testes.

---

## Executando os Testes

### Teste Completo do Fluxo de Perfil

```bash
source venv/bin/activate
python test_profile_flow.py
```

**O que será testado:**
1. Navegação via dropdown desktop
2. Navegação via menu mobile
3. Fluxo completo de edição de perfil
4. Conformidade com design system
5. Responsividade (mobile, tablet, desktop)
6. Segurança e autenticação

**Tempo estimado**: ~60-90 segundos

---

## Saída Esperada

### Sucesso (100% dos testes passando)

```
======================================================================
PROFILE FLOW E2E VALIDATION
Testing navbar dropdown links and complete profile workflow
======================================================================

=== SETUP: Test user ready (teste_profile@finanpy.com) ===

=== TEST 1: Desktop Dropdown Navigation ===
✓ Login successful for teste_profile@finanpy.com
✓ Dropdown opened successfully
✓ Navigation to /profile/ successful
✓ Profile detail page loaded
✓ Navigation to /profile/edit/ successful
✓ Profile edit page loaded

=== TEST 2: Mobile Menu Navigation ===
✓ Mobile menu opened successfully
✓ Navigation to /profile/ successful (mobile)
✓ Navigation to /profile/edit/ successful (mobile)

=== TEST 3: Complete Profile Edit Flow ===
✓ Profile detail page accessible
✓ Edit button navigates to /profile/edit/
✓ Form fields filled successfully
✓ Redirected to profile detail page after save
✓ Success message displayed
✓ All data persisted correctly

=== TEST 4: Design System Compliance ===
✓ Cards with design system classes found
✓ Submit button uses gradient styling
✓ Dropdown follows design system
✓ Screenshot saved: screenshot_dropdown_desktop.png

=== TEST 5: Responsiveness Tests ===
✓ Mobile: No horizontal overflow
✓ Screenshot saved: screenshot_profile_mobile.png
✓ Tablet: No horizontal overflow
✓ Screenshot saved: screenshot_profile_tablet.png
✓ Desktop: No horizontal overflow
✓ Screenshot saved: screenshot_profile_desktop.png

=== TEST 6: Security and Authentication ===
✓ Logout successful
✓ Unauthenticated access properly blocked
✓ Login successful for teste_profile@finanpy.com
✓ User can access own profile
✓ Profile access is isolated to logged-in user (verified in code)

======================================================================
TEST SUMMARY
======================================================================
✓ PASSED: test_desktop_dropdown_navigation
✓ PASSED: test_mobile_menu_navigation
✓ PASSED: test_complete_profile_flow
✓ PASSED: test_design_system_compliance
✓ PASSED: test_responsiveness
✓ PASSED: test_security_and_authentication

Total: 6/6 tests passed (100.0%)

✓ ALL TESTS PASSED - Profile flow validated successfully!
```

---

## Screenshots Geradas

Os testes geram automaticamente 4 screenshots:

1. `screenshot_dropdown_desktop.png` - Dropdown de usuário no desktop
2. `screenshot_profile_mobile.png` - Página de perfil em mobile (375x667)
3. `screenshot_profile_tablet.png` - Página de perfil em tablet (768x1024)
4. `screenshot_profile_desktop.png` - Página de perfil em desktop (1920x1080)

**Localização**: Raiz do projeto

---

## Solução de Problemas

### Erro: "Server not running"

**Problema**: Django server não está rodando

**Solução**:
```bash
# Em outro terminal
source venv/bin/activate
python manage.py runserver
```

---

### Erro: "ModuleNotFoundError: No module named 'playwright'"

**Problema**: Playwright não instalado

**Solução**:
```bash
source venv/bin/activate
pip install playwright
playwright install chromium
```

---

### Erro: "Page.fill: Timeout... #id_email"

**Problema**: Usuário de teste não foi criado

**Solução**: Execute a seção "Criar Usuário de Teste" acima

---

### Erro: "Navigation timeout"

**Problema**: Servidor Django muito lento ou não está respondendo

**Solução**:
1. Verificar se o servidor está rodando: `curl http://localhost:8000/`
2. Reiniciar o servidor Django
3. Limpar cache do navegador: `rm -rf ~/.cache/ms-playwright/`

---

## Executando em Modo Headless

Para executar os testes sem abrir janela do navegador (útil para CI/CD):

Edite `test_profile_flow.py`, linha 370:

```python
# De:
browser = p.chromium.launch(headless=False)

# Para:
browser = p.chromium.launch(headless=True)
```

---

## Estrutura do Script de Teste

```
test_profile_flow.py
├── Helper Functions
│   ├── login() - Faz login do usuário
│   └── logout() - Faz logout do usuário
├── Test Functions
│   ├── test_desktop_dropdown_navigation()
│   ├── test_mobile_menu_navigation()
│   ├── test_complete_profile_flow()
│   ├── test_design_system_compliance()
│   ├── test_responsiveness()
│   └── test_security_and_authentication()
└── run_all_tests() - Executa todos os testes
```

---

## Integrando com CI/CD

Para adicionar estes testes ao pipeline de CI/CD:

### GitHub Actions (exemplo)

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install playwright
          playwright install chromium

      - name: Run migrations
        run: |
          python manage.py migrate

      - name: Create test user
        run: |
          python manage.py shell < create_test_user.py

      - name: Start server
        run: |
          python manage.py runserver &
          sleep 5

      - name: Run E2E tests
        run: |
          python test_profile_flow.py

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: screenshots
          path: screenshot_*.png
```

---

## Mantendo os Testes

### Quando atualizar os testes:

1. **Mudanças na navbar**: Atualizar seletores CSS
2. **Mudanças nas URLs**: Atualizar URLs nos testes
3. **Novos campos no perfil**: Adicionar testes para novos campos
4. **Mudanças no design system**: Atualizar validações de cores/estilos

### Boas práticas:

1. Execute os testes antes de cada commit
2. Execute os testes após mudanças na navbar ou perfil
3. Mantenha screenshots atualizadas
4. Documente falhas nos testes (issues no GitHub)

---

## Relatórios Disponíveis

- **RELATORIO_TESTES_PERFIL.md** - Relatório completo e detalhado
- **SUMARIO_TESTES_PERFIL.md** - Sumário executivo
- **README_TESTES.md** - Este arquivo (guia de execução)

---

## Contato

Para dúvidas sobre os testes, consulte:
- Documentação do Playwright: https://playwright.dev/python/
- PRD do Finanpy: `PRD.md`
- Agent QA Tester: `agents/qa-tester.md`

---

**Última atualização**: 2025-10-29
**Versão dos testes**: 1.0
**Mantido por**: QA Team
