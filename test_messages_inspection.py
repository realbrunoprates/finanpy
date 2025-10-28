"""
Script para inspecionar código e validar implementação do sistema de mensagens.
Este script verifica se todos os elementos necessários estão presentes.
"""

import re
from pathlib import Path

class MessageSystemInspector:
    def __init__(self):
        self.results = []
        self.base_dir = Path('.')

    def log_check(self, component, check_name, passed, details=''):
        status = '✅' if passed else '❌'
        self.results.append({
            'component': component,
            'check': check_name,
            'passed': passed,
            'details': details
        })
        print(f'{status} {component} - {check_name}')
        if details:
            print(f'   {details}')

    def check_base_template(self):
        """Verify base.html has correct message implementation"""
        print('\n=== VERIFICANDO TEMPLATES/BASE.HTML ===\n')

        try:
            with open('templates/base.html', 'r') as f:
                content = f.read()

            # Check 1: Messages block exists
            has_messages_block = '{% if messages %}' in content
            self.log_check('base.html', 'Bloco de mensagens existe', has_messages_block)

            # Check 2: Fixed positioning
            has_fixed_position = 'fixed' in content and 'right-4' in content
            self.log_check('base.html', 'Posicionamento fixed right-4', has_fixed_position)

            # Check 3: Z-index for overlay
            has_z_index = 'z-50' in content
            self.log_check('base.html', 'Z-index 50 para overlay', has_z_index)

            # Check 4: Success message styling
            has_success_style = 'bg-success/10' in content and 'border-success/20' in content
            self.log_check('base.html', 'Estilos SUCCESS (verde)', has_success_style)

            # Check 5: Error message styling
            has_error_style = 'bg-error/10' in content and 'border-error/20' in content
            self.log_check('base.html', 'Estilos ERROR (vermelho)', has_error_style)

            # Check 6: Warning message styling
            has_warning_style = 'bg-warning/10' in content and 'border-warning/20' in content
            self.log_check('base.html', 'Estilos WARNING (amarelo)', has_warning_style)

            # Check 7: Info message styling
            has_info_style = 'bg-info/10' in content and 'border-info/20' in content
            self.log_check('base.html', 'Estilos INFO (azul)', has_info_style)

            # Check 8: Icons for each type
            has_success_icon = content.count('<svg') >= 4
            self.log_check('base.html', 'Ícones SVG para cada tipo de mensagem', has_success_icon,
                          f'Encontrados {content.count("<svg")} ícones SVG')

            # Check 9: Close button
            has_close_button = 'onclick=\'this.parentElement.remove()\'' in content
            self.log_check('base.html', 'Botão de fechar com onclick', has_close_button)

            # Check 10: Auto-hide class
            has_auto_hide = 'auto-hide' in content
            self.log_check('base.html', 'Classe auto-hide presente', has_auto_hide)

            # Check 11: Animation class
            has_animation = 'animate-slide-in' in content
            self.log_check('base.html', 'Classe de animação slide-in', has_animation)

            # Check 12: Animation keyframes
            has_keyframes = '@keyframes slideInRight' in content
            self.log_check('base.html', 'Keyframes slideInRight definidos', has_keyframes)

            # Check 13: Auto-dismiss script
            has_auto_dismiss_script = 'setTimeout' in content and 'auto-hide' in content
            self.log_check('base.html', 'Script de auto-dismiss após 5 segundos', has_auto_dismiss_script)

            # Check 14: Fade out animation
            has_fade_out = 'opacity' in content and 'translateX' in content
            self.log_check('base.html', 'Animação de fade out', has_fade_out)

            # Check 15: Role alert for accessibility
            has_role_alert = 'role=\'alert\'' in content
            self.log_check('base.html', 'role="alert" para acessibilidade', has_role_alert)

            # Check 16: Responsive positioning (top-20 for authenticated, top-4 for not)
            has_responsive_top = 'top-20' in content and 'top-4' in content
            self.log_check('base.html', 'Posicionamento responsivo (top-20/top-4)', has_responsive_top)

            # Check 17: Max width
            has_max_width = 'max-w-md' in content
            self.log_check('base.html', 'Largura máxima (max-w-md)', has_max_width)

            # Check 18: Backdrop blur
            has_backdrop = 'backdrop-blur' in content
            self.log_check('base.html', 'Backdrop blur', has_backdrop)

        except FileNotFoundError:
            self.log_check('base.html', 'Arquivo encontrado', False, 'Arquivo não encontrado')

    def check_users_views(self):
        """Verify users/views.py has message calls"""
        print('\n=== VERIFICANDO USERS/VIEWS.PY ===\n')

        try:
            with open('users/views.py', 'r') as f:
                content = f.read()

            # Check import
            has_import = 'from django.contrib import messages' in content
            self.log_check('users/views.py', 'Import de messages', has_import)

            # Check signup success message
            has_signup_message = 'success_message' in content and 'Conta criada com sucesso' in content
            self.log_check('users/views.py', 'Mensagem de signup', has_signup_message)

            # Check login success message
            has_login_message = 'messages.success' in content and 'Bem-vindo de volta' in content
            self.log_check('users/views.py', 'Mensagem de login', has_login_message)

            # Check logout success message
            has_logout_message = 'saiu com sucesso' in content
            self.log_check('users/views.py', 'Mensagem de logout', has_logout_message)

        except FileNotFoundError:
            self.log_check('users/views.py', 'Arquivo encontrado', False)

    def check_accounts_views(self):
        """Verify accounts/views.py has message calls"""
        print('\n=== VERIFICANDO ACCOUNTS/VIEWS.PY ===\n')

        try:
            with open('accounts/views.py', 'r') as f:
                content = f.read()

            # Check import
            has_import = 'from django.contrib import messages' in content
            self.log_check('accounts/views.py', 'Import de messages', has_import)

            # Check create message
            has_create = 'Conta criada com sucesso' in content
            self.log_check('accounts/views.py', 'Mensagem de criação', has_create)

            # Check update message
            has_update = 'Conta atualizada com sucesso' in content
            self.log_check('accounts/views.py', 'Mensagem de atualização', has_update)

            # Check delete message
            has_delete = 'Conta excluída com sucesso' in content
            self.log_check('accounts/views.py', 'Mensagem de exclusão', has_delete)

        except FileNotFoundError:
            self.log_check('accounts/views.py', 'Arquivo encontrado', False)

    def check_categories_views(self):
        """Verify categories/views.py has message calls"""
        print('\n=== VERIFICANDO CATEGORIES/VIEWS.PY ===\n')

        try:
            with open('categories/views.py', 'r') as f:
                content = f.read()

            # Check import
            has_import = 'from django.contrib import messages' in content
            self.log_check('categories/views.py', 'Import de messages', has_import)

            # Check create message
            has_create = 'Categoria criada com sucesso' in content
            self.log_check('categories/views.py', 'Mensagem de criação', has_create)

            # Check update message
            has_update = 'Categoria atualizada com sucesso' in content
            self.log_check('categories/views.py', 'Mensagem de atualização', has_update)

            # Check delete message
            has_delete = 'Categoria excluída com sucesso' in content
            self.log_check('categories/views.py', 'Mensagem de exclusão', has_delete)

        except FileNotFoundError:
            self.log_check('categories/views.py', 'Arquivo encontrado', False)

    def check_transactions_views(self):
        """Verify transactions/views.py has message calls"""
        print('\n=== VERIFICANDO TRANSACTIONS/VIEWS.PY ===\n')

        try:
            with open('transactions/views.py', 'r') as f:
                content = f.read()

            # Check import
            has_import = 'from django.contrib import messages' in content
            self.log_check('transactions/views.py', 'Import de messages', has_import)

            # Check create success message
            has_create_success = 'messages.success' in content and 'criada com sucesso' in content
            self.log_check('transactions/views.py', 'Mensagem de criação (success)', has_create_success)

            # Check create error message
            has_create_error = 'messages.error' in content and 'Erro ao criar transação' in content
            self.log_check('transactions/views.py', 'Mensagem de erro ao criar', has_create_error)

            # Check update success message
            has_update_success = 'atualizada com sucesso' in content
            self.log_check('transactions/views.py', 'Mensagem de atualização (success)', has_update_success)

            # Check update error message
            has_update_error = 'Erro ao atualizar transação' in content
            self.log_check('transactions/views.py', 'Mensagem de erro ao atualizar', has_update_error)

            # Check delete message
            has_delete = 'excluída com sucesso' in content
            self.log_check('transactions/views.py', 'Mensagem de exclusão', has_delete)

        except FileNotFoundError:
            self.log_check('transactions/views.py', 'Arquivo encontrado', False)

    def check_profiles_views(self):
        """Verify profiles/views.py has message calls"""
        print('\n=== VERIFICANDO PROFILES/VIEWS.PY ===\n')

        try:
            with open('profiles/views.py', 'r') as f:
                content = f.read()

            # Check import
            has_import = 'from django.contrib import messages' in content
            self.log_check('profiles/views.py', 'Import de messages', has_import)

            # Check update message
            has_update = 'Perfil atualizado com sucesso' in content
            self.log_check('profiles/views.py', 'Mensagem de atualização', has_update)

        except FileNotFoundError:
            self.log_check('profiles/views.py', 'Arquivo encontrado', False)

    def check_tailwind_config(self):
        """Verify Tailwind config has correct colors"""
        print('\n=== VERIFICANDO THEME/STATIC_SRC/TAILWIND.CONFIG.JS ===\n')

        try:
            with open('theme/static_src/tailwind.config.js', 'r') as f:
                content = f.read()

            # Check colors
            has_success_color = '#10b981' in content
            self.log_check('tailwind.config.js', 'Cor SUCCESS (#10b981)', has_success_color)

            has_error_color = '#ef4444' in content
            self.log_check('tailwind.config.js', 'Cor ERROR (#ef4444)', has_error_color)

            has_warning_color = '#f59e0b' in content
            self.log_check('tailwind.config.js', 'Cor WARNING (#f59e0b)', has_warning_color)

            has_info_color = '#3b82f6' in content
            self.log_check('tailwind.config.js', 'Cor INFO (#3b82f6)', has_info_color)

        except FileNotFoundError:
            self.log_check('tailwind.config.js', 'Arquivo encontrado', False)

    def print_summary(self):
        """Print inspection summary"""
        print('\n' + '=' * 60)
        print('RESUMO DA INSPEÇÃO DO CÓDIGO')
        print('=' * 60)

        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed

        print(f'Total de Verificações: {total}')
        print(f'Verificações Aprovadas: {passed} ({passed/total*100:.1f}%)')
        print(f'Verificações Falhadas: {failed} ({failed/total*100:.1f}%)')
        print()

        if failed > 0:
            print('VERIFICAÇÕES FALHADAS:')
            for result in self.results:
                if not result['passed']:
                    print(f'  ❌ {result["component"]} - {result["check"]}')
                    if result['details']:
                        print(f'     {result["details"]}')
            print()

        # Group by component
        print('RESUMO POR COMPONENTE:')
        components = {}
        for result in self.results:
            comp = result['component']
            if comp not in components:
                components[comp] = {'passed': 0, 'failed': 0}
            if result['passed']:
                components[comp]['passed'] += 1
            else:
                components[comp]['failed'] += 1

        for comp, stats in components.items():
            total_comp = stats['passed'] + stats['failed']
            percent = stats['passed'] / total_comp * 100
            status = '✅' if stats['failed'] == 0 else ('⚠️' if stats['failed'] <= 2 else '❌')
            print(f'{status} {comp}: {stats["passed"]}/{total_comp} ({percent:.0f}%)')

        print('\n' + '=' * 60)

        if failed == 0:
            print('✅ CÓDIGO TOTALMENTE CONFORME!')
            return 'APROVADO'
        elif failed <= 5:
            print('⚠️  CÓDIGO PARCIALMENTE CONFORME')
            return 'APROVADO COM RESSALVAS'
        else:
            print('❌ CÓDIGO NÃO CONFORME')
            return 'REPROVADO'

    def run_all_inspections(self):
        """Run all code inspections"""
        print('=' * 60)
        print('INSPEÇÃO DE CÓDIGO - SISTEMA DE MENSAGENS FINANPY')
        print('=' * 60)

        self.check_base_template()
        self.check_users_views()
        self.check_accounts_views()
        self.check_categories_views()
        self.check_transactions_views()
        self.check_profiles_views()
        self.check_tailwind_config()

        return self.print_summary()


if __name__ == '__main__':
    inspector = MessageSystemInspector()
    status = inspector.run_all_inspections()
    print(f'\nStatus Final: {status}')
