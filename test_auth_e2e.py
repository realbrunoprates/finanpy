"""
E2E Authentication Testing Script for Finanpy
Tests all authentication flows and validates design system compliance
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'http://localhost:8000'

class TestResults:
    def __init__(self):
        self.tests_passed = []
        self.tests_failed = []
        self.bugs = []
        self.ui_issues = []

    def add_pass(self, test_name, details=''):
        self.tests_passed.append({'name': test_name, 'details': details})
        print(f'✅ PASS: {test_name}')

    def add_fail(self, test_name, details=''):
        self.tests_failed.append({'name': test_name, 'details': details})
        print(f'❌ FAIL: {test_name}')
        print(f'   Details: {details}')

    def add_bug(self, severity, title, description, steps=''):
        bug = {
            'severity': severity,
            'title': title,
            'description': description,
            'steps': steps
        }
        self.bugs.append(bug)
        print(f'🐛 BUG [{severity}]: {title}')

    def add_ui_issue(self, issue):
        self.ui_issues.append(issue)
        print(f'⚠️  UI Issue: {issue}')


def get_csrf_token(session, url):
    """Extract CSRF token from a page"""
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        return csrf_input.get('value')
    return None


def test_server_running(results):
    """Test 1: Verify server is running"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            results.add_pass('Server is running', f'Status code: {response.status_code}')
            return True
        else:
            results.add_fail('Server responded with error', f'Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        results.add_fail('Server is not accessible', str(e))
        return False


def test_home_page(results):
    """Test 2: Home page layout and content"""
    try:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check title
        title = soup.find('title')
        if title and 'Finanpy' in title.text:
            results.add_pass('Home page title is correct', title.text)
        else:
            results.add_fail('Home page title is missing or incorrect')

        # Check for signup button
        signup_link = soup.find('a', href='/auth/signup/')
        if signup_link:
            results.add_pass('Signup button found on home page')
        else:
            results.add_fail('Signup button not found on home page')

        # Check for login button
        login_link = soup.find('a', href='/auth/login/')
        if login_link:
            results.add_pass('Login button found on home page')
        else:
            results.add_fail('Login button not found on home page')

        # Check for gradient classes (design system)
        gradient_elements = soup.find_all(class_=re.compile('gradient'))
        if gradient_elements:
            results.add_pass('Gradient design elements found', f'{len(gradient_elements)} elements')
        else:
            results.add_ui_issue('No gradient elements found - design system may not be applied')

        return True
    except Exception as e:
        results.add_fail('Home page test failed', str(e))
        return False


def test_signup_page_structure(results):
    """Test 3: Signup page structure and fields"""
    try:
        response = requests.get(f'{BASE_URL}/auth/signup/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for email field
        email_field = soup.find('input', {'name': 'email', 'type': 'email'})
        if email_field:
            results.add_pass('Email field found on signup page')
        else:
            results.add_fail('Email field not found on signup page')
            results.add_bug('CRITICAL', 'Missing email field', 'Email input field is not rendered in signup form')

        # Check for username field - CRITICAL for signup
        username_field = soup.find('input', {'name': 'username'})
        if username_field:
            results.add_pass('Username field found on signup page')
        else:
            results.add_fail('Username field not found on signup page')
            results.add_bug(
                'CRITICAL',
                'Missing username field in signup form',
                'The signup form does not include a username field, but the SignupForm requires it. Users cannot register.',
                '1. Navigate to /auth/signup/\n2. Inspect form fields\n3. Notice username field is missing from template'
            )

        # Check for password fields
        password1 = soup.find('input', {'name': 'password1'})
        password2 = soup.find('input', {'name': 'password2'})

        if password1 and password2:
            results.add_pass('Password fields found on signup page')
        else:
            results.add_fail('Password fields incomplete on signup page')

        # Check submit button
        submit_button = soup.find('button', {'type': 'submit'})
        if submit_button:
            results.add_pass('Submit button found on signup page')
        else:
            results.add_fail('Submit button not found on signup page')

        return True
    except Exception as e:
        results.add_fail('Signup page structure test failed', str(e))
        return False


def test_login_page_structure(results):
    """Test 4: Login page structure and fields"""
    try:
        response = requests.get(f'{BASE_URL}/auth/login/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check what field names are actually in the form
        all_inputs = soup.find_all('input')
        field_names = [inp.get('name') for inp in all_inputs if inp.get('name')]

        print(f'   Login form fields found: {field_names}')

        # The LoginForm expects 'email' field but template may have 'username'
        email_field = soup.find('input', {'name': 'email'})
        username_field = soup.find('input', {'name': 'username'})

        if email_field:
            results.add_pass('Email field found on login page')
        elif username_field:
            results.add_fail('Login page uses username field instead of email')
            results.add_bug(
                'CRITICAL',
                'Field name mismatch in login form',
                'Login template uses "username" field but LoginForm expects "email" field. This will cause login to fail.',
                '1. Check users/forms.py LoginForm - uses "email" field\n2. Check templates/auth/login.html - uses "username" in template\n3. Form submission will fail due to missing "email" field'
            )
        else:
            results.add_fail('No email or username field found on login page')

        # Check password field
        password_field = soup.find('input', {'name': 'password', 'type': 'password'})
        if password_field:
            results.add_pass('Password field found on login page')
        else:
            results.add_fail('Password field not found on login page')

        return True
    except Exception as e:
        results.add_fail('Login page structure test failed', str(e))
        return False


def test_invalid_email_registration(results):
    """Test 5: Invalid email validation"""
    session = requests.Session()

    try:
        # Get CSRF token
        csrf_token = get_csrf_token(session, f'{BASE_URL}/auth/signup/')

        # Try to register with invalid email
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'email': 'invalid-email',  # Invalid format
            'password1': 'TesteSenha123!',
            'password2': 'TesteSenha123!',
        }

        # Note: This will fail because username is missing
        response = session.post(f'{BASE_URL}/auth/signup/', data=payload)

        if response.status_code == 200:
            # Check if error message is shown
            soup = BeautifulSoup(response.content, 'html.parser')
            error_text = soup.get_text()

            if 'username' in error_text.lower() and ('obrigatório' in error_text.lower() or 'required' in error_text.lower()):
                results.add_fail('Cannot test email validation - username field error appears first')
                return False
            elif 'e-mail' in error_text.lower() or 'email' in error_text.lower():
                results.add_pass('Invalid email validation works')
                return True

        results.add_fail('Email validation test inconclusive')
        return False

    except Exception as e:
        results.add_fail('Invalid email test failed', str(e))
        return False


def test_authenticated_redirect(results):
    """Test 11: Authenticated user redirect from home"""
    # This would require creating a session with logged-in user
    # Skipping for now as registration is broken
    results.add_fail('Cannot test authenticated redirect - registration is broken')
    return False


def test_design_system_colors(results):
    """Test Design System: Check for design system color classes"""
    try:
        response = requests.get(f'{BASE_URL}/auth/signup/')
        html = response.text

        # Check for design system classes
        checks = {
            'bg-gradient-to-r': 'Gradient background',
            'from-primary-500': 'Primary color gradient start',
            'to-accent-500': 'Accent color gradient end',
            'bg-bg-secondary': 'Secondary background color',
            'text-text-primary': 'Primary text color',
            'border-bg-tertiary': 'Tertiary border color',
            'focus:ring-primary-500': 'Primary focus ring',
        }

        for css_class, description in checks.items():
            if css_class in html:
                results.add_pass(f'Design system: {description}', css_class)
            else:
                results.add_ui_issue(f'Missing design system class: {css_class} ({description})')

        return True
    except Exception as e:
        results.add_fail('Design system test failed', str(e))
        return False


def run_all_tests():
    """Run all authentication tests"""
    print('=' * 80)
    print('FINANPY E2E AUTHENTICATION TESTING')
    print('=' * 80)
    print()

    results = TestResults()

    print('TEST SUITE: Server and Pages')
    print('-' * 80)
    test_server_running(results)
    test_home_page(results)
    test_signup_page_structure(results)
    test_login_page_structure(results)
    print()

    print('TEST SUITE: Form Validations')
    print('-' * 80)
    test_invalid_email_registration(results)
    print()

    print('TEST SUITE: Design System')
    print('-' * 80)
    test_design_system_colors(results)
    print()

    print('=' * 80)
    print('TEST SUMMARY')
    print('=' * 80)
    print(f'Total Passed: {len(results.tests_passed)}')
    print(f'Total Failed: {len(results.tests_failed)}')
    print(f'Total Bugs Found: {len(results.bugs)}')
    print(f'Total UI Issues: {len(results.ui_issues)}')
    print()

    if results.bugs:
        print('=' * 80)
        print('CRITICAL BUGS FOUND')
        print('=' * 80)
        for i, bug in enumerate(results.bugs, 1):
            print(f'\nBUG #{i} [{bug["severity"]}]: {bug["title"]}')
            print(f'Description: {bug["description"]}')
            if bug['steps']:
                print(f'Steps to reproduce:\n{bug["steps"]}')
            print()

    return results


if __name__ == '__main__':
    results = run_all_tests()
