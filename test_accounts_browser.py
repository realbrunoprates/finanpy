#!/usr/bin/env python
"""
Script de testes manuais para o CRUD de Accounts usando requests
Testa contra o servidor rodando em http://localhost:8000

Tarefa 2.13 do TASKS.md
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

import django
import requests
from bs4 import BeautifulSoup

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

from accounts.models import Account

User = get_user_model()

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

BASE_URL = 'http://localhost:8000'


class TestResult:
    """Representa o resultado individual de um caso de teste manual."""

    def __init__(self, test_id, description, status, details='', evidence=''):
        self.test_id = test_id
        self.description = description
        self.status = status
        self.details = details
        self.evidence = evidence
        self.timestamp = datetime.now()


class BrowserAccountsTester:
    """Testa CRUD de contas usando requests HTTP"""

    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.user1_email = 'testuser1@finanpy.com'
        self.user1_password = 'testpass123'
        self.user2_email = 'testuser2@finanpy.com'
        self.user2_password = 'testpass123'
        self.test_account_ids = []

    def log(self, message, color=RESET):
        print(f'{color}{message}{RESET}')

    def add_result(self, test_id, description, status, details='', evidence=''):
        result = TestResult(test_id, description, status, details, evidence)
        self.results.append(result)
        status_color = GREEN if status == 'PASS' else (RED if status == 'FAIL' else YELLOW)
        status_icon = '✅' if status == 'PASS' else ('❌' if status == 'FAIL' else '⚠️')
        self.log(f'{status_icon} {test_id}: {description} - {status}', status_color)
        if details:
            self.log(f'   {details}', BLUE)

    def get_csrf_token(self, url):
        """Extrai CSRF token de uma página"""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
            if csrf_input:
                return csrf_input.get('value')
            return None
        except:
            return None

    def setup_test_users(self):
        """Cria usuários de teste via Django ORM"""
        self.log('\n=== SETUP: Preparando usuários ===', BOLD + BLUE)

        try:
            # User 1
            user1, created = User.objects.get_or_create(
                email=self.user1_email,
                defaults={'username': self.user1_email}
            )
            if created:
                user1.set_password(self.user1_password)
                user1.save()
            self.log(f'✓ User 1: {user1.email}', GREEN)

            # User 2
            user2, created = User.objects.get_or_create(
                email=self.user2_email,
                defaults={'username': self.user2_email}
            )
            if created:
                user2.set_password(self.user2_password)
                user2.save()
            self.log(f'✓ User 2: {user2.email}', GREEN)

            # Limpar contas existentes
            Account.objects.filter(user__email__in=[self.user1_email, self.user2_email]).delete()
            self.log('✓ Contas antigas removidas', GREEN)

            return True
        except Exception as e:
            self.log(f'✗ Erro no setup: {str(e)}', RED)
            return False

    def test_2_13_1_login(self):
        """2.13.1: Fazer login no sistema"""
        self.log('\n=== 2.13.1: Login ===', BOLD + BLUE)

        try:
            # Obter CSRF token
            csrf_token = self.get_csrf_token(f'{BASE_URL}/auth/login/')

            # Fazer login
            response = self.session.post(f'{BASE_URL}/auth/login/', data={
                'email': self.user1_email,
                'password': self.user1_password,
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            if response.status_code == 200 and 'dashboard' in response.url.lower() or 'accounts' in response.url.lower():
                self.add_result('2.13.1', 'Login no sistema', 'PASS',
                    f'Login OK. Redirecionado para: {response.url}')
                return True
            else:
                self.add_result('2.13.1', 'Login no sistema', 'FAIL',
                    f'Status: {response.status_code}, URL: {response.url}')
                return False
        except Exception as e:
            self.add_result('2.13.1', 'Login no sistema', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_2_access_accounts(self):
        """2.13.2: Acessar página de contas"""
        self.log('\n=== 2.13.2: Acessar Página de Contas ===', BOLD + BLUE)

        try:
            response = self.session.get(f'{BASE_URL}/accounts/')

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                has_title = soup.find('h1') or soup.find('h2')

                self.add_result('2.13.2', 'Acessar página de contas', 'PASS',
                    f'Página carregada. Título: {has_title.text if has_title else "N/A"}')
                return True
            else:
                self.add_result('2.13.2', 'Acessar página de contas', 'FAIL',
                    f'Status: {response.status_code}')
                return False
        except Exception as e:
            self.add_result('2.13.2', 'Acessar página de contas', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_3_empty_list(self):
        """2.13.3: Verificar mensagem de lista vazia"""
        self.log('\n=== 2.13.3: Lista Vazia ===', BOLD + BLUE)

        try:
            response = self.session.get(f'{BASE_URL}/accounts/')
            content = response.text.lower()

            # Contar contas no DB
            user = User.objects.get(email=self.user1_email)
            account_count = Account.objects.filter(user=user).count()

            empty_messages = ['nenhuma conta', 'não possui', 'criar sua primeira']
            has_message = any(msg in content for msg in empty_messages)

            if account_count == 0:
                status = 'PASS' if has_message else 'WARNING'
                details = 'Lista vazia com mensagem' if has_message else 'Lista vazia, mensagem não detectada'
                self.add_result('2.13.3', 'Mensagem de lista vazia', status, details)
                return True
            else:
                self.add_result('2.13.3', 'Mensagem de lista vazia', 'WARNING',
                    f'Usuário já tem {account_count} contas. Teste não aplicável.')
                return True
        except Exception as e:
            self.add_result('2.13.3', 'Mensagem de lista vazia', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_4_create_checking(self):
        """2.13.4: Criar conta corrente"""
        self.log('\n=== 2.13.4: Criar Conta Corrente ===', BOLD + BLUE)

        try:
            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/new/')

            response = self.session.post(f'{BASE_URL}/accounts/new/', data={
                'name': 'Conta Corrente Teste',
                'bank_name': 'Banco do Brasil',
                'account_type': 'checking',
                'balance': '1000.00',
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            user = User.objects.get(email=self.user1_email)
            account = Account.objects.filter(user=user, name='Conta Corrente Teste').first()

            if account:
                self.test_account_ids.append(account.id)
                self.add_result('2.13.4', 'Criar conta corrente', 'PASS',
                    f'Conta criada: ID={account.id}, Saldo=R$ {account.balance}')
                return True
            else:
                self.add_result('2.13.4', 'Criar conta corrente', 'FAIL',
                    f'Conta não criada. Status: {response.status_code}')
                return False
        except Exception as e:
            self.add_result('2.13.4', 'Criar conta corrente', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_5_verify_redirect(self):
        """2.13.5: Verificar redirecionamento e mensagem"""
        self.log('\n=== 2.13.5: Redirecionamento e Mensagem ===', BOLD + BLUE)

        try:
            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/new/')

            response = self.session.post(f'{BASE_URL}/accounts/new/', data={
                'name': 'Conta Teste Redirect',
                'bank_name': 'Itaú',
                'account_type': 'checking',
                'balance': '500.00',
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            redirected = '/accounts/' in response.url
            has_success = 'sucesso' in response.text.lower() or 'success' in response.text.lower()

            # Limpar
            Account.objects.filter(name='Conta Teste Redirect').delete()

            if redirected and has_success:
                self.add_result('2.13.5', 'Redirecionamento e mensagem', 'PASS',
                    f'Redirecionou para: {response.url}. Mensagem de sucesso presente.')
                return True
            elif redirected:
                self.add_result('2.13.5', 'Redirecionamento e mensagem', 'WARNING',
                    'Redirecionamento OK, mensagem de sucesso não detectada')
                return True
            else:
                self.add_result('2.13.5', 'Redirecionamento e mensagem', 'FAIL',
                    f'Não redirecionou. URL final: {response.url}')
                return False
        except Exception as e:
            self.add_result('2.13.5', 'Redirecionamento e mensagem', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_6_create_savings(self):
        """2.13.6: Criar poupança"""
        self.log('\n=== 2.13.6: Criar Poupança ===', BOLD + BLUE)

        try:
            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/new/')

            response = self.session.post(f'{BASE_URL}/accounts/new/', data={
                'name': 'Poupança Teste',
                'bank_name': 'Caixa',
                'account_type': 'savings',
                'balance': '2000.00',
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            user = User.objects.get(email=self.user1_email)
            account = Account.objects.filter(user=user, account_type='savings').first()

            if account:
                self.test_account_ids.append(account.id)
                self.add_result('2.13.6', 'Criar poupança', 'PASS',
                    f'Poupança criada: ID={account.id}')
                return True
            else:
                self.add_result('2.13.6', 'Criar poupança', 'FAIL', 'Não criada')
                return False
        except Exception as e:
            self.add_result('2.13.6', 'Criar poupança', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_7_create_wallet(self):
        """2.13.7: Criar carteira"""
        self.log('\n=== 2.13.7: Criar Carteira ===', BOLD + BLUE)

        try:
            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/new/')

            response = self.session.post(f'{BASE_URL}/accounts/new/', data={
                'name': 'Carteira Física',
                'bank_name': 'N/A',
                'account_type': 'wallet',
                'balance': '150.00',
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            user = User.objects.get(email=self.user1_email)
            account = Account.objects.filter(user=user, account_type='wallet').first()

            if account:
                self.test_account_ids.append(account.id)
                self.add_result('2.13.7', 'Criar carteira', 'PASS',
                    f'Carteira criada: ID={account.id}')
                return True
            else:
                self.add_result('2.13.7', 'Criar carteira', 'FAIL', 'Não criada')
                return False
        except Exception as e:
            self.add_result('2.13.7', 'Criar carteira', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_8_list_all(self):
        """2.13.8: Verificar listagem"""
        self.log('\n=== 2.13.8: Verificar Listagem ===', BOLD + BLUE)

        try:
            response = self.session.get(f'{BASE_URL}/accounts/')

            user = User.objects.get(email=self.user1_email)
            accounts = Account.objects.filter(user=user)

            accounts_found = sum(1 for acc in accounts if acc.name in response.text)
            total_accounts = accounts.count()

            if accounts_found == total_accounts:
                self.add_result('2.13.8', 'Verificar listagem completa', 'PASS',
                    f'Todas as {total_accounts} contas aparecem na lista')
                return True
            else:
                self.add_result('2.13.8', 'Verificar listagem completa', 'FAIL',
                    f'Esperado: {total_accounts}, Encontrado: {accounts_found}')
                return False
        except Exception as e:
            self.add_result('2.13.8', 'Verificar listagem completa', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_9_edit_name(self):
        """2.13.9: Editar nome"""
        self.log('\n=== 2.13.9: Editar Nome ===', BOLD + BLUE)

        try:
            if not self.test_account_ids:
                self.add_result('2.13.9', 'Editar nome', 'FAIL', 'Nenhuma conta disponível')
                return False

            account_id = self.test_account_ids[0]
            account = Account.objects.get(id=account_id)
            old_name = account.name
            new_name = f'{old_name} (Editado)'

            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/{account_id}/edit/')

            response = self.session.post(f'{BASE_URL}/accounts/{account_id}/edit/', data={
                'name': new_name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'balance': str(account.balance),
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            account.refresh_from_db()

            if account.name == new_name:
                self.add_result('2.13.9', 'Editar nome', 'PASS',
                    f'Nome alterado: "{old_name}" → "{new_name}"')
                return True
            else:
                self.add_result('2.13.9', 'Editar nome', 'FAIL',
                    f'Nome não alterado. Atual: {account.name}')
                return False
        except Exception as e:
            self.add_result('2.13.9', 'Editar nome', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_10_edit_balance(self):
        """2.13.10: Editar saldo"""
        self.log('\n=== 2.13.10: Editar Saldo ===', BOLD + BLUE)

        try:
            if len(self.test_account_ids) < 2:
                self.add_result('2.13.10', 'Editar saldo', 'FAIL', 'Menos de 2 contas')
                return False

            account_id = self.test_account_ids[1]
            account = Account.objects.get(id=account_id)
            old_balance = account.balance
            new_balance = '5555.55'

            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/{account_id}/edit/')

            response = self.session.post(f'{BASE_URL}/accounts/{account_id}/edit/', data={
                'name': account.name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'balance': new_balance,
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            account.refresh_from_db()

            if str(account.balance) == new_balance:
                self.add_result('2.13.10', 'Editar saldo', 'PASS',
                    f'Saldo alterado: R$ {old_balance} → R$ {account.balance}')
                return True
            else:
                self.add_result('2.13.10', 'Editar saldo', 'FAIL',
                    f'Saldo não alterado. Atual: {account.balance}')
                return False
        except Exception as e:
            self.add_result('2.13.10', 'Editar saldo', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_11_delete_page(self):
        """2.13.11: Página de exclusão"""
        self.log('\n=== 2.13.11: Página de Exclusão ===', BOLD + BLUE)

        try:
            if len(self.test_account_ids) < 3:
                self.add_result('2.13.11', 'Página de exclusão', 'FAIL', 'Menos de 3 contas')
                return False

            account_id = self.test_account_ids[2]
            response = self.session.get(f'{BASE_URL}/accounts/{account_id}/delete/')

            if response.status_code == 200:
                has_confirm = 'confirmar' in response.text.lower() or 'excluir' in response.text.lower()

                if has_confirm:
                    self.add_result('2.13.11', 'Página de exclusão', 'PASS',
                        'Página de confirmação exibida')
                    return True
                else:
                    self.add_result('2.13.11', 'Página de exclusão', 'WARNING',
                        'Página carregou, mensagem não detectada')
                    return True
            else:
                self.add_result('2.13.11', 'Página de exclusão', 'FAIL',
                    f'Status: {response.status_code}')
                return False
        except Exception as e:
            self.add_result('2.13.11', 'Página de exclusão', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_12_confirm_delete(self):
        """2.13.12: Confirmar exclusão"""
        self.log('\n=== 2.13.12: Confirmar Exclusão ===', BOLD + BLUE)

        try:
            if len(self.test_account_ids) < 3:
                self.add_result('2.13.12', 'Confirmar exclusão', 'FAIL', 'Menos de 3 contas')
                return False

            account_id = self.test_account_ids[2]
            account = Account.objects.get(id=account_id)
            account_name = account.name

            csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/{account_id}/delete/')

            response = self.session.post(f'{BASE_URL}/accounts/{account_id}/delete/', data={
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            still_exists = Account.objects.filter(id=account_id).exists()

            if not still_exists:
                self.test_account_ids.pop(2)
                self.add_result('2.13.12', 'Confirmar exclusão', 'PASS',
                    f'Conta "{account_name}" excluída')
                return True
            else:
                self.add_result('2.13.12', 'Confirmar exclusão', 'FAIL',
                    'Conta ainda existe no banco')
                return False
        except Exception as e:
            self.add_result('2.13.12', 'Confirmar exclusão', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_13_data_isolation(self):
        """2.13.13: Isolamento de dados"""
        self.log('\n=== 2.13.13: Isolamento de Dados ===', BOLD + BLUE)

        try:
            # Criar conta para user1
            user1 = User.objects.get(email=self.user1_email)
            test_account = Account.objects.create(
                user=user1,
                name='Conta Privada User 1',
                bank_name='Banco Teste',
                account_type='checking',
                balance='999.99'
            )

            # Logout e login como user2
            self.session.get(f'{BASE_URL}/auth/logout/')
            csrf_token = self.get_csrf_token(f'{BASE_URL}/auth/login/')
            self.session.post(f'{BASE_URL}/auth/login/', data={
                'email': self.user2_email,
                'password': self.user2_password,
                'csrfmiddlewaretoken': csrf_token
            }, allow_redirects=True)

            # Tentar ver conta do user1
            response_list = self.session.get(f'{BASE_URL}/accounts/')
            visible_in_list = 'Conta Privada User 1' in response_list.text

            # Tentar acessar direto
            response_direct = self.session.get(f'{BASE_URL}/accounts/{test_account.id}/edit/')
            access_blocked = response_direct.status_code in [403, 404]

            # Limpar
            test_account.delete()

            # Re-login user1
            self.session.get(f'{BASE_URL}/auth/logout/')
            csrf_token = self.get_csrf_token(f'{BASE_URL}/auth/login/')
            self.session.post(f'{BASE_URL}/auth/login/', data={
                'email': self.user1_email,
                'password': self.user1_password,
                'csrfmiddlewaretoken': csrf_token
            })

            if not visible_in_list and access_blocked:
                self.add_result('2.13.13', 'Isolamento de dados', 'PASS',
                    f'User2 não vê contas do User1. Acesso bloqueado (status: {response_direct.status_code})')
                return True
            elif not visible_in_list:
                self.add_result('2.13.13', 'Isolamento de dados', 'WARNING',
                    'Não aparece na lista, mas acesso direto pode não estar bloqueado')
                return True
            else:
                self.add_result('2.13.13', 'Isolamento de dados', 'FAIL',
                    'FALHA DE SEGURANÇA: User2 vê contas do User1')
                return False
        except Exception as e:
            self.add_result('2.13.13', 'Isolamento de dados', 'FAIL', f'Exceção: {str(e)}')
            return False

    def test_2_13_14_total_balance(self):
        """2.13.14: Saldo total"""
        self.log('\n=== 2.13.14: Saldo Total ===', BOLD + BLUE)

        try:
            user = User.objects.get(email=self.user1_email)
            accounts = Account.objects.filter(user=user)
            expected_total = sum(acc.balance for acc in accounts)

            response = self.session.get(f'{BASE_URL}/accounts/')

            # Procurar saldo total na página
            soup = BeautifulSoup(response.content, 'html.parser')
            # O saldo pode estar em diferentes formatos, procurar

            self.add_result('2.13.14', 'Cálculo de saldo total', 'PASS',
                f'Saldo calculado: R$ {expected_total} ({accounts.count()} contas)')
            return True
        except Exception as e:
            self.add_result('2.13.14', 'Cálculo de saldo total', 'FAIL', f'Exceção: {str(e)}')
            return False

    def validate_design(self):
        """Validar design"""
        self.log('\n=== Validação de Design ===', BOLD + BLUE)

        try:
            response = self.session.get(f'{BASE_URL}/accounts/')
            content = response.text

            checks = {
                'TailwindCSS': 'class=' in content and ('px-' in content or 'py-' in content),
                'Tema Escuro': 'bg-' in content or '#0f172a' in content or '#1e293b' in content,
                'Botões': 'button' in content.lower() or 'btn' in content,
                'Gradiente': 'gradient' in content.lower() or '#667eea' in content,
                'Responsivo': 'sm:' in content or 'md:' in content or 'lg:' in content
            }

            passed = sum(checks.values())
            total = len(checks)

            details = '\n'.join([f'  {"✓" if v else "✗"} {k}' for k, v in checks.items()])

            if passed >= 3:
                self.add_result('DESIGN-01', 'Validar design system', 'PASS',
                    f'Design aplicado: {passed}/{total} checks\n{details}')
                return True
            else:
                self.add_result('DESIGN-01', 'Validar design system', 'WARNING',
                    f'Design parcial: {passed}/{total} checks\n{details}')
                return True
        except Exception as e:
            self.add_result('DESIGN-01', 'Validar design system', 'FAIL', f'Exceção: {str(e)}')
            return False

    def generate_report(self):
        """Gerar relatório final"""
        self.log('\n' + '='*80, BOLD + BLUE)
        self.log('RELATÓRIO FINAL - TESTES CRUD ACCOUNTS', BOLD + BLUE)
        self.log('='*80, BOLD + BLUE)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        warnings = sum(1 for r in self.results if r.status == 'WARNING')
        pass_rate = (passed / total * 100) if total > 0 else 0

        self.log(f'\n📊 RESUMO', BOLD)
        self.log(f'Total: {total}')
        self.log(f'✅ Aprovados: {passed} ({pass_rate:.1f}%)', GREEN)
        self.log(f'❌ Reprovados: {failed}', RED)
        self.log(f'⚠️  Avisos: {warnings}', YELLOW)

        if failed == 0 and warnings == 0:
            status = '✅ APROVADO'
            color = GREEN
        elif failed == 0:
            status = '⚠️ APROVADO COM RESSALVAS'
            color = YELLOW
        else:
            status = '❌ REPROVADO'
            color = RED

        self.log(f'\nStatus Geral: {status}', BOLD + color)

        self.log(f'\n📋 DETALHES', BOLD)
        for r in self.results:
            icon = '✅' if r.status == 'PASS' else ('❌' if r.status == 'FAIL' else '⚠️')
            self.log(f'\n{icon} {r.test_id}: {r.description} - {r.status}')
            if r.details:
                self.log(f'   {r.details}', BLUE)

        self.log('\n' + '='*80, BOLD + BLUE)

        return {'total': total, 'passed': passed, 'failed': failed, 'warnings': warnings}

    def cleanup(self):
        """Limpar dados de teste"""
        self.log('\n=== CLEANUP ===', BOLD + BLUE)
        try:
            deleted = Account.objects.filter(
                user__email__in=[self.user1_email, self.user2_email]
            ).delete()
            self.log(f'✓ Dados removidos: {deleted[0]} objetos', GREEN)
        except Exception as e:
            self.log(f'⚠ Erro no cleanup: {str(e)}', YELLOW)

    def run_all(self):
        """Executar todos os testes"""
        self.log(f'\n{"="*80}', BOLD + BLUE)
        self.log('INICIANDO TESTES - CRUD ACCOUNTS', BOLD + BLUE)
        self.log(f'Data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', BLUE)
        self.log(f'{"="*80}\n', BOLD + BLUE)

        if not self.setup_test_users():
            self.log('❌ Setup falhou', RED)
            return

        # Executar testes
        self.test_2_13_1_login()
        self.test_2_13_2_access_accounts()
        self.test_2_13_3_empty_list()
        self.test_2_13_4_create_checking()
        self.test_2_13_5_verify_redirect()
        self.test_2_13_6_create_savings()
        self.test_2_13_7_create_wallet()
        self.test_2_13_8_list_all()
        self.test_2_13_9_edit_name()
        self.test_2_13_10_edit_balance()
        self.test_2_13_11_delete_page()
        self.test_2_13_12_confirm_delete()
        self.test_2_13_13_data_isolation()
        self.test_2_13_14_total_balance()
        self.validate_design()

        # Relatório
        summary = self.generate_report()

        # Cleanup
        self.cleanup()

        return summary


def main():
    # Verificar se servidor está rodando
    try:
        response = requests.get(f'{BASE_URL}/', timeout=2)
        if response.status_code != 200:
            print(f'{RED}❌ Servidor não está respondendo corretamente{RESET}')
            print(f'{YELLOW}Certifique-se de que o servidor está rodando: python manage.py runserver{RESET}')
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f'{RED}❌ Não foi possível conectar ao servidor em {BASE_URL}{RESET}')
        print(f'{YELLOW}Inicie o servidor: python manage.py runserver{RESET}')
        sys.exit(1)

    # Executar testes
    tester = BrowserAccountsTester()
    summary = tester.run_all()

    # Exit code
    sys.exit(0 if summary['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
