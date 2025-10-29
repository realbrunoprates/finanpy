"""
Script automatizado para testar o sistema de mensagens do Finanpy.
Executa testes funcionais e valida a presença de mensagens Django.
"""
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://localhost:8000'
TEST_EMAIL = 'qa.tester@finanpy.com'
TEST_PASSWORD = 'TestPass123!'

class MessageTester:
    """Executa cenários para validar mensagens exibidas pela aplicação."""

    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.csrf_token = None

    def log_test(self, test_name, passed, details=''):
        """Log test result"""
        status = '✅ PASSOU' if passed else '❌ FALHOU'
        result = {
            'test': test_name,
            'status': status,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        print(f'{status} - {test_name}')
        if details:
            print(f'  Details: {details}')

    def get_csrf_token(self, url):
        """Extract CSRF token from page"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if csrf_input:
            return csrf_input.get('value')
        return None

    def check_message_in_response(self, response, expected_text=None, message_type=None):
        """Check if Django message exists in response"""
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find message containers
        messages = soup.find_all('div', class_=lambda x: x and 'auto-hide' in x)

        if not messages:
            return False, 'Nenhuma mensagem encontrada'

        for msg in messages:
            msg_text = msg.get_text(strip=True)

            # Check text if provided
            if expected_text and expected_text in msg_text:
                # Check message type (class contains bg-success, bg-error, etc)
                if message_type:
                    classes = msg.get('class', [])
                    type_class = f'bg-{message_type}/10'
                    # Check if message has correct type styling
                    class_str = ' '.join(classes)
                    if message_type in class_str or type_class in class_str:
                        return True, f'Mensagem encontrada com tipo correto: {message_type}'
                    else:
                        return False, f'Mensagem encontrada mas tipo incorreto. Esperado: {message_type}'
                return True, 'Mensagem encontrada'

        return False, f'Mensagem não encontrada. Esperado: {expected_text}'

    def test_login_success(self):
        """Test login success message"""
        test_name = 'Login com Sucesso - Mensagem "Bem-vindo de volta!"'

        # Get login page to obtain CSRF token
        csrf_token = self.get_csrf_token(f'{BASE_URL}/login/')

        if not csrf_token:
            self.log_test(test_name, False, 'CSRF token não encontrado')
            return False

        # Perform login
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD
        }

        response = self.session.post(
            f'{BASE_URL}/login/',
            data=login_data,
            allow_redirects=True
        )

        # Check for success message
        has_message, details = self.check_message_in_response(
            response,
            expected_text='Bem-vindo de volta',
            message_type='success'
        )

        self.log_test(test_name, has_message, details)
        return has_message

    def test_account_create_success(self):
        """Test account creation success message"""
        test_name = 'Criar Conta - Mensagem "Conta criada com sucesso!"'

        # Get create account page
        csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/create/')

        if not csrf_token:
            self.log_test(test_name, False, 'CSRF token não encontrado')
            return False

        # Create account
        account_data = {
            'csrfmiddlewaretoken': csrf_token,
            'name': f'Conta Teste Automatizado {int(time.time())}',
            'account_type': 'checking',
            'balance': '1000.00'
        }

        response = self.session.post(
            f'{BASE_URL}/accounts/create/',
            data=account_data,
            allow_redirects=True
        )

        # Check for success message
        has_message, details = self.check_message_in_response(
            response,
            expected_text='Conta criada com sucesso',
            message_type='success'
        )

        self.log_test(test_name, has_message, details)
        return has_message

    def test_category_create_success(self):
        """Test category creation success message"""
        test_name = 'Criar Categoria - Mensagem "Categoria criada com sucesso!"'

        # Get create category page
        csrf_token = self.get_csrf_token(f'{BASE_URL}/categories/create/')

        if not csrf_token:
            self.log_test(test_name, False, 'CSRF token não encontrado')
            return False

        # Create category
        category_data = {
            'csrfmiddlewaretoken': csrf_token,
            'name': f'Categoria Teste {int(time.time())}',
            'category_type': 'expense'
        }

        response = self.session.post(
            f'{BASE_URL}/categories/create/',
            data=category_data,
            allow_redirects=True
        )

        # Check for success message
        has_message, details = self.check_message_in_response(
            response,
            expected_text='Categoria criada com sucesso',
            message_type='success'
        )

        self.log_test(test_name, has_message, details)
        return has_message

    def test_profile_update_success(self):
        """Test profile update success message"""
        test_name = 'Atualizar Perfil - Mensagem "Perfil atualizado com sucesso!"'

        # Get profile edit page
        csrf_token = self.get_csrf_token(f'{BASE_URL}/profile/edit/')

        if not csrf_token:
            self.log_test(test_name, False, 'CSRF token não encontrado')
            return False

        # Update profile
        profile_data = {
            'csrfmiddlewaretoken': csrf_token,
            'phone': '11999998888',
            'bio': 'QA Tester - Automated Test'
        }

        response = self.session.post(
            f'{BASE_URL}/profile/edit/',
            data=profile_data,
            allow_redirects=True
        )

        # Check for success message
        has_message, details = self.check_message_in_response(
            response,
            expected_text='Perfil atualizado com sucesso',
            message_type='success'
        )

        self.log_test(test_name, has_message, details)
        return has_message

    def test_logout_success(self):
        """Test logout success message"""
        test_name = 'Logout - Mensagem "Você saiu com sucesso."'

        # Get logout page (might need CSRF from another page)
        csrf_token = self.get_csrf_token(f'{BASE_URL}/accounts/')

        # Perform logout
        response = self.session.post(
            f'{BASE_URL}/logout/',
            data={'csrfmiddlewaretoken': csrf_token} if csrf_token else {},
            allow_redirects=True
        )

        # Check for success message
        has_message, details = self.check_message_in_response(
            response,
            expected_text='saiu com sucesso',
            message_type='success'
        )

        self.log_test(test_name, has_message, details)
        return has_message

    def check_message_structure(self):
        """Verify message HTML structure in base template"""
        test_name = 'Estrutura HTML de Mensagens no base.html'

        response = self.session.get(f'{BASE_URL}/')

        # We can't directly check base.html, but we can verify rendered page structure
        # This is more of a code inspection test

        with open('templates/base.html', 'r') as f:
            base_content = f.read()

            checks = [
                ('fixed' in base_content, 'Posicionamento fixed'),
                ('right-4' in base_content, 'Posicionamento right-4'),
                ('z-50' in base_content, 'Z-index 50'),
                ('auto-hide' in base_content, 'Classe auto-hide'),
                ('animate-slide-in' in base_content, 'Animação slide-in'),
                ('role=\'alert\'' in base_content, 'Role alert para acessibilidade'),
                ('bg-success/10' in base_content, 'Cor SUCCESS'),
                ('bg-error/10' in base_content, 'Cor ERROR'),
                ('bg-warning/10' in base_content, 'Cor WARNING'),
                ('bg-info/10' in base_content, 'Cor INFO'),
            ]

            all_passed = all([check[0] for check in checks])
            failed_checks = [check[1] for check in checks if not check[0]]

            details = 'Todos os checks passaram' if all_passed else f'Checks falhados: {", ".join(failed_checks)}'
            self.log_test(test_name, all_passed, details)

            return all_passed

    def run_all_tests(self):
        """Run all tests in sequence"""
        print('=' * 60)
        print('INICIANDO TESTES AUTOMATIZADOS DO SISTEMA DE MENSAGENS')
        print('=' * 60)
        print()

        # Test 1: Login
        print('--- Teste 1: Autenticação ---')
        self.test_login_success()
        print()

        # Test 2: Account Create
        print('--- Teste 2: Contas ---')
        self.test_account_create_success()
        print()

        # Test 3: Category Create
        print('--- Teste 3: Categorias ---')
        self.test_category_create_success()
        print()

        # Test 4: Profile Update
        print('--- Teste 4: Perfil ---')
        self.test_profile_update_success()
        print()

        # Test 5: Logout
        print('--- Teste 5: Logout ---')
        self.test_logout_success()
        print()

        # Test 6: Structure
        print('--- Teste 6: Estrutura HTML ---')
        self.check_message_structure()
        print()

        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print('=' * 60)
        print('RESUMO DOS TESTES')
        print('=' * 60)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed

        print(f'Total de Testes: {total}')
        print(f'Testes Aprovados: {passed} ({passed/total*100:.1f}%)')
        print(f'Testes Falhados: {failed} ({failed/total*100:.1f}%)')
        print()

        if failed > 0:
            print('TESTES FALHADOS:')
            for result in self.test_results:
                if not result['passed']:
                    print(f'  ❌ {result["test"]}')
                    print(f'     {result["details"]}')

        print()

        if failed == 0:
            print('✅ TODOS OS TESTES PASSARAM!')
            print('Status: APROVADO')
        elif failed <= 2:
            print('⚠️  ALGUNS TESTES FALHARAM')
            print('Status: APROVADO COM RESSALVAS')
        else:
            print('❌ MUITOS TESTES FALHARAM')
            print('Status: REPROVADO')

        print('=' * 60)


if __name__ == '__main__':
    tester = MessageTester()
    tester.run_all_tests()
