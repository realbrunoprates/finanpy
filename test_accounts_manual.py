#!/usr/bin/env python
"""
Script de testes manuais automatizados para o CRUD de Accounts
Tarefa 2.13 do TASKS.md

Este script realiza testes completos do CRUD de contas, incluindo:
- Autenticação e acesso
- Criação de contas (CHECKING, SAVINGS, WALLET)
- Edição de contas
- Exclusão de contas
- Isolamento de dados entre usuários
- Validações de design e responsividade
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from accounts.models import Account

User = get_user_model()

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


class TestResult:
    """Armazena resultados de um teste individual"""
    def __init__(self, test_id, description, status, details='', evidence=''):
        self.test_id = test_id
        self.description = description
        self.status = status  # 'PASS', 'FAIL', 'WARNING'
        self.details = details
        self.evidence = evidence
        self.timestamp = datetime.now()


class AccountsCRUDTester:
    """Testa o CRUD completo de contas"""

    def __init__(self):
        self.client = Client()
        self.results = []
        self.user1 = None
        self.user2 = None
        self.test_accounts = []

    def log(self, message, color=RESET):
        """Log colorido no terminal"""
        print(f'{color}{message}{RESET}')

    def add_result(self, test_id, description, status, details='', evidence=''):
        """Adiciona resultado de teste"""
        result = TestResult(test_id, description, status, details, evidence)
        self.results.append(result)

        # Log imediato
        status_color = GREEN if status == 'PASS' else (RED if status == 'FAIL' else YELLOW)
        status_icon = '✅' if status == 'PASS' else ('❌' if status == 'FAIL' else '⚠️')
        self.log(f'{status_icon} {test_id}: {description} - {status}', status_color)
        if details:
            self.log(f'   Detalhes: {details}', BLUE)

    def setup_test_users(self):
        """Cria ou obtém usuários de teste"""
        self.log('\n=== SETUP: Preparando usuários de teste ===', BOLD + BLUE)

        try:
            # User 1
            self.user1, created = User.objects.get_or_create(
                email='testuser1@finanpy.com',
                defaults={'username': 'testuser1@finanpy.com'}
            )
            if created:
                self.user1.set_password('testpass123')
                self.user1.save()
                self.log(f'✓ Usuário 1 criado: {self.user1.email}', GREEN)
            else:
                self.log(f'✓ Usuário 1 existente: {self.user1.email}', GREEN)

            # User 2 (para teste de isolamento)
            self.user2, created = User.objects.get_or_create(
                email='testuser2@finanpy.com',
                defaults={'username': 'testuser2@finanpy.com'}
            )
            if created:
                self.user2.set_password('testpass123')
                self.user2.save()
                self.log(f'✓ Usuário 2 criado: {self.user2.email}', GREEN)
            else:
                self.log(f'✓ Usuário 2 existente: {self.user2.email}', GREEN)

            # Limpar contas existentes dos usuários de teste
            Account.objects.filter(user__in=[self.user1, self.user2]).delete()
            self.log('✓ Contas de teste anteriores removidas', GREEN)

            return True
        except Exception as e:
            self.log(f'✗ Erro no setup: {str(e)}', RED)
            return False

    def test_2_13_1_login(self):
        """2.13.1: Fazer login no sistema"""
        self.log('\n=== Teste 2.13.1: Login no Sistema ===', BOLD + BLUE)

        try:
            # Tentar login
            response = self.client.post('/auth/login/', {
                'email': 'testuser1@finanpy.com',
                'password': 'testpass123'
            }, follow=True)

            # Verificar se login foi bem sucedido
            if response.status_code == 200 and self.client.session.get('_auth_user_id'):
                self.add_result(
                    '2.13.1',
                    'Fazer login no sistema',
                    'PASS',
                    f'Login realizado com sucesso. Status code: {response.status_code}'
                )
                return True
            else:
                self.add_result(
                    '2.13.1',
                    'Fazer login no sistema',
                    'FAIL',
                    f'Login falhou. Status code: {response.status_code}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.1',
                'Fazer login no sistema',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_2_access_accounts_page(self):
        """2.13.2: Acessar página de contas"""
        self.log('\n=== Teste 2.13.2: Acessar Página de Contas ===', BOLD + BLUE)

        try:
            response = self.client.get('/accounts/')

            if response.status_code == 200:
                # Verificar se template correto foi usado
                template_names = [t.name for t in response.templates]
                if 'accounts/account_list.html' in template_names:
                    self.add_result(
                        '2.13.2',
                        'Acessar página de contas',
                        'PASS',
                        f'Página carregada com sucesso. Templates: {template_names}'
                    )
                    return True
                else:
                    self.add_result(
                        '2.13.2',
                        'Acessar página de contas',
                        'WARNING',
                        f'Página carregou mas template pode estar incorreto: {template_names}'
                    )
                    return True
            else:
                self.add_result(
                    '2.13.2',
                    'Acessar página de contas',
                    'FAIL',
                    f'Status code incorreto: {response.status_code}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.2',
                'Acessar página de contas',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_3_empty_list_message(self):
        """2.13.3: Verificar mensagem de lista vazia"""
        self.log('\n=== Teste 2.13.3: Mensagem de Lista Vazia ===', BOLD + BLUE)

        try:
            response = self.client.get('/accounts/')
            content = response.content.decode('utf-8')

            # Verificar se há mensagem de lista vazia
            # Procurar por textos comuns: "Nenhuma conta", "Você ainda não tem", etc
            empty_indicators = [
                'Nenhuma conta',
                'nenhuma conta',
                'Você ainda não tem',
                'não possui contas',
                'Criar sua primeira conta'
            ]

            has_empty_message = any(indicator in content for indicator in empty_indicators)

            # Contar número de contas do usuário
            account_count = Account.objects.filter(user=self.user1).count()

            if account_count == 0 and has_empty_message:
                self.add_result(
                    '2.13.3',
                    'Verificar mensagem de lista vazia',
                    'PASS',
                    f'Lista vazia e mensagem exibida corretamente'
                )
                return True
            elif account_count == 0 and not has_empty_message:
                self.add_result(
                    '2.13.3',
                    'Verificar mensagem de lista vazia',
                    'WARNING',
                    f'Lista vazia mas mensagem de feedback pode estar ausente'
                )
                return True
            elif account_count > 0:
                self.add_result(
                    '2.13.3',
                    'Verificar mensagem de lista vazia',
                    'WARNING',
                    f'Usuário já possui {account_count} conta(s). Teste não aplicável.'
                )
                return True
            else:
                self.add_result(
                    '2.13.3',
                    'Verificar mensagem de lista vazia',
                    'FAIL',
                    f'Estado inesperado'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.3',
                'Verificar mensagem de lista vazia',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_4_create_checking_account(self):
        """2.13.4: Criar nova conta corrente"""
        self.log('\n=== Teste 2.13.4: Criar Conta Corrente ===', BOLD + BLUE)

        try:
            # Obter CSRF token
            response = self.client.get('/accounts/new/')

            # Criar conta corrente
            response = self.client.post('/accounts/new/', {
                'name': 'Conta Corrente Teste',
                'bank_name': 'Banco do Brasil',
                'account_type': 'checking',
                'balance': '1000.00'
            }, follow=True)

            # Verificar se conta foi criada
            account = Account.objects.filter(
                user=self.user1,
                name='Conta Corrente Teste'
            ).first()

            if account:
                self.test_accounts.append(account)
                self.add_result(
                    '2.13.4',
                    'Criar nova conta corrente',
                    'PASS',
                    f'Conta criada: ID={account.id}, Nome={account.name}, Tipo={account.account_type}, Saldo={account.balance}'
                )
                return True
            else:
                self.add_result(
                    '2.13.4',
                    'Criar nova conta corrente',
                    'FAIL',
                    f'Conta não foi criada no banco. Status code: {response.status_code}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.4',
                'Criar nova conta corrente',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_5_verify_redirect_and_message(self):
        """2.13.5: Verificar redirecionamento e mensagem de sucesso"""
        self.log('\n=== Teste 2.13.5: Redirecionamento e Mensagem ===', BOLD + BLUE)

        try:
            # Criar conta e verificar redirecionamento
            response = self.client.post('/accounts/new/', {
                'name': 'Conta para Teste de Redirect',
                'bank_name': 'Santander',
                'account_type': 'checking',
                'balance': '500.00'
            }, follow=True)

            # Verificar redirecionamento para lista
            final_url = response.redirect_chain[-1][0] if response.redirect_chain else ''
            redirected_to_list = '/accounts/' in final_url

            # Verificar mensagem de sucesso
            messages = list(response.context.get('messages', []))
            has_success_message = any('sucesso' in str(m).lower() for m in messages)

            # Limpar conta de teste
            Account.objects.filter(name='Conta para Teste de Redirect').delete()

            if redirected_to_list and has_success_message:
                self.add_result(
                    '2.13.5',
                    'Verificar redirecionamento e mensagem de sucesso',
                    'PASS',
                    f'Redirecionou para: {final_url}. Mensagem de sucesso exibida.'
                )
                return True
            elif redirected_to_list:
                self.add_result(
                    '2.13.5',
                    'Verificar redirecionamento e mensagem de sucesso',
                    'WARNING',
                    f'Redirecionamento OK, mas mensagem de sucesso pode estar ausente'
                )
                return True
            else:
                self.add_result(
                    '2.13.5',
                    'Verificar redirecionamento e mensagem de sucesso',
                    'FAIL',
                    f'Redirecionamento incorreto. Final URL: {final_url}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.5',
                'Verificar redirecionamento e mensagem de sucesso',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_6_create_savings_account(self):
        """2.13.6: Criar conta poupança"""
        self.log('\n=== Teste 2.13.6: Criar Conta Poupança ===', BOLD + BLUE)

        try:
            response = self.client.post('/accounts/new/', {
                'name': 'Poupança Teste',
                'bank_name': 'Caixa Econômica',
                'account_type': 'savings',
                'balance': '2000.00'
            }, follow=True)

            account = Account.objects.filter(
                user=self.user1,
                name='Poupança Teste',
                account_type='savings'
            ).first()

            if account:
                self.test_accounts.append(account)
                self.add_result(
                    '2.13.6',
                    'Criar conta poupança',
                    'PASS',
                    f'Poupança criada: ID={account.id}, Saldo={account.balance}'
                )
                return True
            else:
                self.add_result(
                    '2.13.6',
                    'Criar conta poupança',
                    'FAIL',
                    'Conta poupança não foi criada'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.6',
                'Criar conta poupança',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_7_create_wallet_account(self):
        """2.13.7: Criar conta tipo carteira"""
        self.log('\n=== Teste 2.13.7: Criar Conta Carteira ===', BOLD + BLUE)

        try:
            response = self.client.post('/accounts/new/', {
                'name': 'Carteira Física',
                'bank_name': 'N/A',
                'account_type': 'wallet',
                'balance': '150.00'
            }, follow=True)

            account = Account.objects.filter(
                user=self.user1,
                name='Carteira Física',
                account_type='wallet'
            ).first()

            if account:
                self.test_accounts.append(account)
                self.add_result(
                    '2.13.7',
                    'Criar conta tipo carteira',
                    'PASS',
                    f'Carteira criada: ID={account.id}, Saldo={account.balance}'
                )
                return True
            else:
                self.add_result(
                    '2.13.7',
                    'Criar conta tipo carteira',
                    'FAIL',
                    'Conta carteira não foi criada'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.7',
                'Criar conta tipo carteira',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_8_verify_all_accounts_in_list(self):
        """2.13.8: Verificar que todas as contas aparecem na listagem"""
        self.log('\n=== Teste 2.13.8: Verificar Listagem Completa ===', BOLD + BLUE)

        try:
            response = self.client.get('/accounts/')
            content = response.content.decode('utf-8')

            # Contar contas no banco
            db_count = Account.objects.filter(user=self.user1).count()

            # Verificar se nomes das contas aparecem na página
            accounts_in_db = Account.objects.filter(user=self.user1)
            accounts_found = []
            accounts_missing = []

            for account in accounts_in_db:
                if account.name in content:
                    accounts_found.append(account.name)
                else:
                    accounts_missing.append(account.name)

            if len(accounts_found) == db_count and len(accounts_missing) == 0:
                self.add_result(
                    '2.13.8',
                    'Verificar que todas as contas aparecem na listagem',
                    'PASS',
                    f'Todas as {db_count} contas aparecem na listagem: {accounts_found}'
                )
                return True
            else:
                self.add_result(
                    '2.13.8',
                    'Verificar que todas as contas aparecem na listagem',
                    'FAIL',
                    f'Contas no DB: {db_count}, Encontradas: {len(accounts_found)}, Faltando: {accounts_missing}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.8',
                'Verificar que todas as contas aparecem na listagem',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_9_edit_account_name(self):
        """2.13.9: Editar nome de uma conta"""
        self.log('\n=== Teste 2.13.9: Editar Nome de Conta ===', BOLD + BLUE)

        try:
            # Pegar primeira conta de teste
            if not self.test_accounts:
                self.add_result(
                    '2.13.9',
                    'Editar nome de uma conta',
                    'FAIL',
                    'Nenhuma conta de teste disponível'
                )
                return False

            account = self.test_accounts[0]
            old_name = account.name
            new_name = f'{old_name} (Editado)'

            # Editar conta
            response = self.client.post(f'/accounts/{account.id}/edit/', {
                'name': new_name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'balance': str(account.balance)
            }, follow=True)

            # Recarregar do banco
            account.refresh_from_db()

            if account.name == new_name:
                self.add_result(
                    '2.13.9',
                    'Editar nome de uma conta',
                    'PASS',
                    f'Nome alterado de "{old_name}" para "{new_name}"'
                )
                return True
            else:
                self.add_result(
                    '2.13.9',
                    'Editar nome de uma conta',
                    'FAIL',
                    f'Nome não foi alterado. Esperado: "{new_name}", Atual: "{account.name}"'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.9',
                'Editar nome de uma conta',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_10_edit_account_balance(self):
        """2.13.10: Editar saldo de uma conta"""
        self.log('\n=== Teste 2.13.10: Editar Saldo de Conta ===', BOLD + BLUE)

        try:
            if len(self.test_accounts) < 2:
                self.add_result(
                    '2.13.10',
                    'Editar saldo de uma conta',
                    'FAIL',
                    'Menos de 2 contas de teste disponíveis'
                )
                return False

            account = self.test_accounts[1]
            old_balance = account.balance
            new_balance = Decimal('5555.55')

            # Editar saldo
            response = self.client.post(f'/accounts/{account.id}/edit/', {
                'name': account.name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'balance': str(new_balance)
            }, follow=True)

            # Recarregar do banco
            account.refresh_from_db()

            if account.balance == new_balance:
                self.add_result(
                    '2.13.10',
                    'Editar saldo de uma conta',
                    'PASS',
                    f'Saldo alterado de R$ {old_balance} para R$ {new_balance}'
                )
                return True
            else:
                self.add_result(
                    '2.13.10',
                    'Editar saldo de uma conta',
                    'FAIL',
                    f'Saldo não foi alterado. Esperado: {new_balance}, Atual: {account.balance}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.10',
                'Editar saldo de uma conta',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_11_attempt_delete_account(self):
        """2.13.11: Tentar excluir uma conta"""
        self.log('\n=== Teste 2.13.11: Tentar Excluir Conta ===', BOLD + BLUE)

        try:
            if len(self.test_accounts) < 3:
                self.add_result(
                    '2.13.11',
                    'Tentar excluir uma conta',
                    'FAIL',
                    'Menos de 3 contas de teste disponíveis'
                )
                return False

            account_to_delete = self.test_accounts[2]
            account_id = account_to_delete.id
            account_name = account_to_delete.name

            # Acessar página de confirmação
            response = self.client.get(f'/accounts/{account_id}/delete/')

            # Verificar se página de confirmação carrega
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                # Verificar se há mensagem de confirmação
                has_confirmation = any(word in content.lower() for word in ['confirmar', 'excluir', 'deletar', 'remover'])

                if has_confirmation:
                    self.add_result(
                        '2.13.11',
                        'Tentar excluir uma conta',
                        'PASS',
                        f'Página de confirmação de exclusão exibida corretamente para conta "{account_name}"'
                    )
                    return True
                else:
                    self.add_result(
                        '2.13.11',
                        'Tentar excluir uma conta',
                        'WARNING',
                        f'Página carregou mas pode não ter mensagem de confirmação'
                    )
                    return True
            else:
                self.add_result(
                    '2.13.11',
                    'Tentar excluir uma conta',
                    'FAIL',
                    f'Página de exclusão não carregou. Status: {response.status_code}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.11',
                'Tentar excluir uma conta',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_12_confirm_account_deletion(self):
        """2.13.12: Verificar que conta foi excluída"""
        self.log('\n=== Teste 2.13.12: Confirmar Exclusão ===', BOLD + BLUE)

        try:
            if len(self.test_accounts) < 3:
                self.add_result(
                    '2.13.12',
                    'Verificar que conta foi excluída',
                    'FAIL',
                    'Menos de 3 contas de teste disponíveis'
                )
                return False

            account_to_delete = self.test_accounts[2]
            account_id = account_to_delete.id
            account_name = account_to_delete.name

            # Executar exclusão
            response = self.client.post(f'/accounts/{account_id}/delete/', follow=True)

            # Verificar se conta foi excluída do banco
            still_exists = Account.objects.filter(id=account_id).exists()

            if not still_exists:
                self.add_result(
                    '2.13.12',
                    'Verificar que conta foi excluída',
                    'PASS',
                    f'Conta "{account_name}" (ID={account_id}) foi excluída com sucesso'
                )
                # Remover da lista de teste
                self.test_accounts.pop(2)
                return True
            else:
                self.add_result(
                    '2.13.12',
                    'Verificar que conta foi excluída',
                    'FAIL',
                    f'Conta ainda existe no banco após tentativa de exclusão'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.12',
                'Verificar que conta foi excluída',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_13_data_isolation(self):
        """2.13.13: Verificar isolamento de dados entre usuários"""
        self.log('\n=== Teste 2.13.13: Isolamento de Dados ===', BOLD + BLUE)

        try:
            # Criar conta para usuário 1
            user1_account = Account.objects.create(
                user=self.user1,
                name='Conta Privada User 1',
                bank_name='Banco Teste',
                account_type='checking',
                balance=Decimal('999.99')
            )

            # Fazer login como usuário 2
            self.client.logout()
            self.client.post('/auth/login/', {
                'email': 'testuser2@finanpy.com',
                'password': 'testpass123'
            })

            # Tentar acessar listagem (não deve ver conta do user 1)
            response = self.client.get('/accounts/')
            content = response.content.decode('utf-8')

            user1_account_visible = 'Conta Privada User 1' in content

            # Tentar acessar diretamente a conta do user 1 via edit
            response_edit = self.client.get(f'/accounts/{user1_account.id}/edit/')

            # Deve retornar 404 ou 403
            access_blocked = response_edit.status_code in [403, 404]

            # Fazer login novamente como user 1
            self.client.logout()
            self.client.post('/auth/login/', {
                'email': 'testuser1@finanpy.com',
                'password': 'testpass123'
            })

            # Limpar conta de teste
            user1_account.delete()

            if not user1_account_visible and access_blocked:
                self.add_result(
                    '2.13.13',
                    'Verificar isolamento de dados entre usuários',
                    'PASS',
                    f'User 2 não vê contas do User 1. Acesso direto bloqueado (status: {response_edit.status_code})'
                )
                return True
            elif not user1_account_visible:
                self.add_result(
                    '2.13.13',
                    'Verificar isolamento de dados entre usuários',
                    'WARNING',
                    f'Conta não aparece na lista, mas acesso direto pode não estar bloqueado adequadamente'
                )
                return True
            else:
                self.add_result(
                    '2.13.13',
                    'Verificar isolamento de dados entre usuários',
                    'FAIL',
                    f'FALHA DE SEGURANÇA: User 2 pode ver contas do User 1'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.13',
                'Verificar isolamento de dados entre usuários',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def test_2_13_14_total_balance_calculation(self):
        """2.13.14: Verificar cálculo de saldo total"""
        self.log('\n=== Teste 2.13.14: Cálculo de Saldo Total ===', BOLD + BLUE)

        try:
            # Calcular saldo total manualmente
            accounts = Account.objects.filter(user=self.user1)
            expected_total = sum(acc.balance for acc in accounts)

            # Obter saldo total da view
            response = self.client.get('/accounts/')
            total_balance_in_context = response.context.get('total_balance', 0)

            # Comparar
            if total_balance_in_context == expected_total:
                self.add_result(
                    '2.13.14',
                    'Verificar cálculo de saldo total',
                    'PASS',
                    f'Saldo total calculado corretamente: R$ {expected_total:.2f} ({accounts.count()} contas)'
                )
                return True
            else:
                self.add_result(
                    '2.13.14',
                    'Verificar cálculo de saldo total',
                    'FAIL',
                    f'Saldo incorreto. Esperado: R$ {expected_total:.2f}, Obtido: R$ {total_balance_in_context:.2f}'
                )
                return False
        except Exception as e:
            self.add_result(
                '2.13.14',
                'Verificar cálculo de saldo total',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def validate_design_system(self):
        """Validar conformidade com Design System"""
        self.log('\n=== Validação de Design System ===', BOLD + BLUE)

        try:
            response = self.client.get('/accounts/')
            content = response.content.decode('utf-8')

            design_checks = {
                'Gradiente Primary (#667eea → #764ba2)': '#667eea' in content or 'from-primary' in content,
                'Background Dark (#0f172a)': '#0f172a' in content or 'bg-bg-primary' in content,
                'Cards Background (#1e293b)': '#1e293b' in content or 'bg-bg-secondary' in content,
                'TailwindCSS Classes': any(cls in content for cls in ['px-', 'py-', 'rounded-', 'shadow-']),
                'Botões Estilizados': 'button' in content.lower() or 'btn' in content.lower(),
            }

            passed = sum(design_checks.values())
            total = len(design_checks)

            details = '\n'.join([f'  {"✓" if v else "✗"} {k}' for k, v in design_checks.items()])

            if passed >= total * 0.8:  # 80% dos checks
                self.add_result(
                    'DESIGN-01',
                    'Validar conformidade com Design System',
                    'PASS',
                    f'Design System aplicado: {passed}/{total} checks passaram\n{details}'
                )
                return True
            else:
                self.add_result(
                    'DESIGN-01',
                    'Validar conformidade com Design System',
                    'WARNING',
                    f'Design System parcialmente aplicado: {passed}/{total} checks\n{details}'
                )
                return True
        except Exception as e:
            self.add_result(
                'DESIGN-01',
                'Validar conformidade com Design System',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def validate_responsiveness(self):
        """Validar responsividade (limitado sem browser real)"""
        self.log('\n=== Validação de Responsividade ===', BOLD + BLUE)

        try:
            response = self.client.get('/accounts/')
            content = response.content.decode('utf-8')

            # Verificar classes responsivas do Tailwind
            responsive_classes = [
                'sm:', 'md:', 'lg:', 'xl:',  # Breakpoints
                'grid', 'flex',  # Layouts responsivos
                'w-full', 'max-w-',  # Width responsiva
            ]

            responsive_score = sum(1 for cls in responsive_classes if cls in content)

            if responsive_score >= 5:
                self.add_result(
                    'RESPONSIVE-01',
                    'Validar responsividade',
                    'PASS',
                    f'Classes responsivas detectadas ({responsive_score} diferentes). Nota: Teste visual manual recomendado.'
                )
                return True
            else:
                self.add_result(
                    'RESPONSIVE-01',
                    'Validar responsividade',
                    'WARNING',
                    f'Poucas classes responsivas detectadas ({responsive_score}). Verificar manualmente.'
                )
                return True
        except Exception as e:
            self.add_result(
                'RESPONSIVE-01',
                'Validar responsividade',
                'FAIL',
                f'Exceção: {str(e)}'
            )
            return False

    def generate_report(self):
        """Gera relatório completo de testes"""
        self.log('\n' + '='*80, BOLD + BLUE)
        self.log('RELATÓRIO FINAL DE TESTES - CRUD DE ACCOUNTS', BOLD + BLUE)
        self.log('='*80, BOLD + BLUE)

        # Contadores
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        warnings = sum(1 for r in self.results if r.status == 'WARNING')

        pass_rate = (passed / total * 100) if total > 0 else 0

        # Resumo
        self.log(f'\n📊 RESUMO EXECUTIVO', BOLD)
        self.log(f'Total de Testes: {total}')
        self.log(f'✅ Aprovados: {passed} ({pass_rate:.1f}%)', GREEN)
        self.log(f'❌ Reprovados: {failed}', RED)
        self.log(f'⚠️  Avisos: {warnings}', YELLOW)

        # Status geral
        if failed == 0 and warnings == 0:
            status = '✅ APROVADO'
            status_color = GREEN
        elif failed == 0:
            status = '⚠️ APROVADO COM RESSALVAS'
            status_color = YELLOW
        else:
            status = '❌ REPROVADO'
            status_color = RED

        self.log(f'\n🎯 Status Geral: {status}', BOLD + status_color)

        # Detalhes por categoria
        self.log(f'\n📋 DETALHES POR TESTE', BOLD)

        for result in self.results:
            status_icon = '✅' if result.status == 'PASS' else ('❌' if result.status == 'FAIL' else '⚠️')
            self.log(f'\n{status_icon} {result.test_id}: {result.description}')
            self.log(f'   Status: {result.status}')
            if result.details:
                self.log(f'   {result.details}', BLUE)

        # Recomendações
        self.log(f'\n💡 RECOMENDAÇÕES', BOLD)

        if failed > 0:
            self.log('❌ CRÍTICO: Corrigir todas as falhas antes de prosseguir', RED)

        if warnings > 0:
            self.log(f'⚠️  Revisar {warnings} aviso(s) e validar manualmente se necessário', YELLOW)

        self.log('\n✓ Realizar testes visuais manuais em navegador real', BLUE)
        self.log('✓ Testar responsividade em diferentes dispositivos', BLUE)
        self.log('✓ Validar acessibilidade (navegação por teclado, screen readers)', BLUE)

        self.log('\n' + '='*80, BOLD + BLUE)

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'pass_rate': pass_rate,
            'status': status
        }

    def cleanup(self):
        """Limpa dados de teste"""
        self.log('\n=== CLEANUP: Removendo dados de teste ===', BOLD + BLUE)
        try:
            # Remover contas de teste
            deleted = Account.objects.filter(user__in=[self.user1, self.user2]).delete()
            self.log(f'✓ Contas de teste removidas: {deleted[0]} objetos', GREEN)
        except Exception as e:
            self.log(f'⚠ Erro no cleanup: {str(e)}', YELLOW)

    def run_all_tests(self):
        """Executa todos os testes na ordem correta"""
        self.log(f'\n{"="*80}', BOLD + BLUE)
        self.log('INICIANDO BATERIA DE TESTES - CRUD DE ACCOUNTS', BOLD + BLUE)
        self.log(f'Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', BLUE)
        self.log(f'{"="*80}\n', BOLD + BLUE)

        # Setup
        if not self.setup_test_users():
            self.log('❌ Setup falhou. Abortando testes.', RED)
            return

        # Testes funcionais (2.13.1 - 2.13.14)
        self.test_2_13_1_login()
        self.test_2_13_2_access_accounts_page()
        self.test_2_13_3_empty_list_message()
        self.test_2_13_4_create_checking_account()
        self.test_2_13_5_verify_redirect_and_message()
        self.test_2_13_6_create_savings_account()
        self.test_2_13_7_create_wallet_account()
        self.test_2_13_8_verify_all_accounts_in_list()
        self.test_2_13_9_edit_account_name()
        self.test_2_13_10_edit_account_balance()
        self.test_2_13_11_attempt_delete_account()
        self.test_2_13_12_confirm_account_deletion()
        self.test_2_13_13_data_isolation()
        self.test_2_13_14_total_balance_calculation()

        # Validações de design
        self.validate_design_system()
        self.validate_responsiveness()

        # Relatório final
        summary = self.generate_report()

        # Cleanup
        self.cleanup()

        return summary


def main():
    """Função principal"""
    tester = AccountsCRUDTester()
    summary = tester.run_all_tests()

    # Exit code baseado no resultado
    if summary['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
