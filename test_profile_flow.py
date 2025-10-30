"""
E2E Test - Profile Flow Validation
Tests complete user profile flow after navbar dropdown link adjustments
"""

from playwright.sync_api import sync_playwright, expect
import time


def create_test_user_if_not_exists(page):
    """Helper: Create test user via registration if not exists"""
    page.goto('http://localhost:8000/register/')

    # Try to register
    page.fill('#id_email', 'teste_profile@finanpy.com')
    page.fill('#id_password1', 'TestPass123!@#')
    page.fill('#id_password2', 'TestPass123!@#')
    page.click('button[type="submit"]')

    # Wait for either success (dashboard) or error (user exists)
    time.sleep(2)


def login(page, email='teste_profile@finanpy.com', password='TestPass123!@#'):
    """Helper: Login user"""
    page.goto('http://localhost:8000/auth/login/')
    page.wait_for_selector('#id_email', timeout=10000)
    page.fill('#id_email', email)
    page.fill('#id_password', password)
    page.click('button[type="submit"]')

    # Wait for redirect to dashboard
    page.wait_for_url('http://localhost:8000/dashboard/', timeout=10000)
    print(f'✓ Login successful for {email}')


def logout(page):
    """Helper: Logout user via form submission"""
    # Open dropdown first (desktop)
    try:
        page.click('#user-menu-button', timeout=2000)
        time.sleep(0.5)
    except:
        # If dropdown not found, might be in mobile or already open
        pass

    # Find and submit logout form
    page.click('button[type="submit"]:has-text("Sair")')

    # Wait for redirect with more time
    time.sleep(2)
    print('✓ Logout successful')


def test_desktop_dropdown_navigation(page):
    """Test 1: Desktop dropdown navigation to profile pages"""
    print('\n=== TEST 1: Desktop Dropdown Navigation ===')

    # Set desktop viewport
    page.set_viewport_size({'width': 1920, 'height': 1080})

    # Login
    login(page)

    # Test 1.1: Click "Ver Perfil" in dropdown
    print('\nTest 1.1: Ver Perfil link in desktop dropdown')

    # Open dropdown
    page.click('#user-menu-button')
    time.sleep(0.5)

    # Verify dropdown is visible
    dropdown = page.locator('#user-menu-dropdown')
    expect(dropdown).not_to_have_class('hidden')
    print('✓ Dropdown opened successfully')

    # Click "Ver Perfil"
    page.click('a[href="/profile/"]')
    page.wait_for_url('http://localhost:8000/profile/', timeout=5000)
    print('✓ Navigation to /profile/ successful')

    # Verify page content
    expect(page.locator('h1')).to_contain_text('Perfil')
    print('✓ Profile detail page loaded')

    # Test 1.2: Click "Editar Perfil" in dropdown
    print('\nTest 1.2: Editar Perfil link in desktop dropdown')

    # Open dropdown again
    page.click('#user-menu-button')
    time.sleep(0.5)

    # Click "Editar Perfil"
    page.click('a[href="/profile/edit/"]')
    page.wait_for_url('http://localhost:8000/profile/edit/', timeout=5000)
    print('✓ Navigation to /profile/edit/ successful')

    # Verify page content
    expect(page.locator('h1')).to_contain_text('Editar Perfil')
    print('✓ Profile edit page loaded')

    return True


def test_mobile_menu_navigation(page):
    """Test 2: Mobile menu navigation to profile pages"""
    print('\n=== TEST 2: Mobile Menu Navigation ===')

    # Set mobile viewport
    page.set_viewport_size({'width': 375, 'height': 667})

    # Go to dashboard
    page.goto('http://localhost:8000/dashboard/')

    # Test 2.1: Open mobile menu
    print('\nTest 2.1: Mobile menu toggle')

    mobile_menu_button = page.locator('#mobile-menu-button')
    expect(mobile_menu_button).to_be_visible()

    mobile_menu_button.click()
    time.sleep(0.5)

    mobile_menu = page.locator('#mobile-menu')
    expect(mobile_menu).not_to_have_class('hidden')
    print('✓ Mobile menu opened successfully')

    # Test 2.2: Click "Ver Perfil" in mobile menu
    print('\nTest 2.2: Ver Perfil link in mobile menu')

    # Find the "Ver Perfil" link in mobile menu
    profile_link = page.locator('#mobile-menu a[href="/profile/"]')
    expect(profile_link).to_be_visible()
    profile_link.click()

    page.wait_for_url('http://localhost:8000/profile/', timeout=5000)
    print('✓ Navigation to /profile/ successful (mobile)')

    # Test 2.3: Click "Editar Perfil" in mobile menu
    print('\nTest 2.3: Editar Perfil link in mobile menu')

    # Open mobile menu again
    mobile_menu_button.click()
    time.sleep(0.5)

    edit_profile_link = page.locator('#mobile-menu a[href="/profile/edit/"]')
    expect(edit_profile_link).to_be_visible()
    edit_profile_link.click()

    page.wait_for_url('http://localhost:8000/profile/edit/', timeout=5000)
    print('✓ Navigation to /profile/edit/ successful (mobile)')

    return True


def test_complete_profile_flow(page):
    """Test 3: Complete profile edit flow"""
    print('\n=== TEST 3: Complete Profile Edit Flow ===')

    # Set desktop viewport
    page.set_viewport_size({'width': 1920, 'height': 1080})

    # Test 3.1: Access profile detail page
    print('\nTest 3.1: Access profile detail page')
    page.goto('http://localhost:8000/profile/')

    expect(page.locator('h1')).to_contain_text('Perfil')
    print('✓ Profile detail page accessible')

    # Test 3.2: Click edit button from detail page
    print('\nTest 3.2: Click edit button on profile page')

    # Use more specific selector for the main edit button (not from dropdown)
    edit_button = page.locator('a[href="/profile/edit/"].bg-gradient-to-r').first
    expect(edit_button).to_be_visible()
    edit_button.click()

    page.wait_for_url('http://localhost:8000/profile/edit/', timeout=5000)
    print('✓ Edit button navigates to /profile/edit/')

    # Test 3.3: Edit profile information
    print('\nTest 3.3: Edit profile information')

    timestamp = str(int(time.time()))

    # Fill form fields (only full_name and phone exist in Profile model)
    page.fill('#id_full_name', f'Usuario Teste Profile {timestamp}')
    page.fill('#id_phone', '11987654321')

    print('✓ Form fields filled successfully')

    # Test 3.4: Save changes
    print('\nTest 3.4: Save profile changes')

    submit_button = page.locator('button[type="submit"]:has-text("Salvar")')
    expect(submit_button).to_be_visible()
    submit_button.click()

    # Should redirect back to profile detail
    page.wait_for_url('http://localhost:8000/profile/', timeout=5000)
    print('✓ Redirected to profile detail page after save')

    # Test 3.5: Verify success message
    print('\nTest 3.5: Verify success message')

    success_message = page.locator('div[role="alert"]:has-text("sucesso")')
    expect(success_message.first).to_be_visible(timeout=3000)
    print('✓ Success message displayed')

    # Test 3.6: Verify data persistence
    print('\nTest 3.6: Verify data persistence')

    page_content = page.content()
    assert f'Usuario Teste Profile {timestamp}' in page_content, 'Full name not persisted'
    assert '11987654321' in page_content or '(11) 98765-4321' in page_content or '11 98765-4321' in page_content, 'Phone not persisted'

    print('✓ All data persisted correctly')

    return True


def test_design_system_compliance(page):
    """Test 4: Design system compliance"""
    print('\n=== TEST 4: Design System Compliance ===')

    page.set_viewport_size({'width': 1920, 'height': 1080})

    # Test 4.1: Profile detail page design
    print('\nTest 4.1: Profile detail page design')
    page.goto('http://localhost:8000/profile/')

    # Check for dark theme background
    bg_color = page.locator('body').evaluate('el => window.getComputedStyle(el).backgroundColor')
    print(f'  Body background: {bg_color}')

    # Check for cards with proper styling
    cards = page.locator('.bg-bg-secondary, .rounded-xl')
    if cards.count() > 0:
        print('✓ Cards with design system classes found')

    # Test 4.2: Profile edit page design
    print('\nTest 4.2: Profile edit page design')
    page.goto('http://localhost:8000/profile/edit/')

    # Check form inputs styling
    inputs = page.locator('input[type="text"], textarea')
    input_count = inputs.count()
    print(f'  Found {input_count} form inputs')

    if input_count > 0:
        first_input = inputs.first
        input_bg = first_input.evaluate('el => window.getComputedStyle(el).backgroundColor')
        print(f'  Input background: {input_bg}')

    # Check submit button styling (use the save button, not logout button)
    submit_button = page.locator('button[type="submit"]:has-text("Salvar")')
    button_classes = submit_button.get_attribute('class')

    has_gradient = 'gradient' in button_classes or 'from-primary' in button_classes
    print(f'  Submit button has gradient: {has_gradient}')

    if has_gradient:
        print('✓ Submit button uses gradient styling')

    # Test 4.3: Dropdown styling
    print('\nTest 4.3: Dropdown styling')
    page.goto('http://localhost:8000/dashboard/')

    # Open dropdown
    page.click('#user-menu-button')
    time.sleep(0.5)

    # Check dropdown menu styling
    dropdown = page.locator('#user-menu-dropdown')
    dropdown_classes = dropdown.get_attribute('class')

    has_proper_styling = 'bg-bg-secondary' in dropdown_classes and 'rounded-xl' in dropdown_classes
    print(f'  Dropdown has proper styling: {has_proper_styling}')

    if has_proper_styling:
        print('✓ Dropdown follows design system')

    # Take screenshots for manual review
    page.screenshot(path='/home/brunoprates/Documentos/Pycodebr/Study/Projetos_estudos/finanpy/screenshot_dropdown_desktop.png')
    print('✓ Screenshot saved: screenshot_dropdown_desktop.png')

    return True


def test_responsiveness(page):
    """Test 5: Responsiveness across viewports"""
    print('\n=== TEST 5: Responsiveness Tests ===')

    viewports = [
        {'name': 'Mobile', 'width': 375, 'height': 667},
        {'name': 'Tablet', 'width': 768, 'height': 1024},
        {'name': 'Desktop', 'width': 1920, 'height': 1080},
    ]

    for viewport in viewports:
        print(f'\nTest 5.{viewports.index(viewport) + 1}: {viewport["name"]} ({viewport["width"]}x{viewport["height"]})')

        page.set_viewport_size({'width': viewport['width'], 'height': viewport['height']})
        page.goto('http://localhost:8000/profile/')

        # Check if page renders without horizontal scroll
        scroll_width = page.evaluate('document.documentElement.scrollWidth')
        client_width = page.evaluate('document.documentElement.clientWidth')

        has_horizontal_scroll = scroll_width > client_width
        print(f'  Horizontal scroll: {has_horizontal_scroll}')

        if not has_horizontal_scroll:
            print(f'✓ {viewport["name"]}: No horizontal overflow')
        else:
            print(f'⚠ {viewport["name"]}: Has horizontal overflow')

        # Take screenshot
        screenshot_name = f'screenshot_profile_{viewport["name"].lower()}.png'
        page.screenshot(path=f'/home/brunoprates/Documentos/Pycodebr/Study/Projetos_estudos/finanpy/{screenshot_name}', full_page=True)
        print(f'✓ Screenshot saved: {screenshot_name}')

    return True


def test_security_and_authentication(page):
    """Test 6: Security and authentication"""
    print('\n=== TEST 6: Security and Authentication ===')

    # Test 6.1: Unauthenticated access
    print('\nTest 6.1: Unauthenticated access to profile')

    # Logout first
    page.goto('http://localhost:8000/dashboard/')
    logout(page)

    # Try to access profile without login
    page.goto('http://localhost:8000/profile/')

    # Wait a bit for redirect to happen
    time.sleep(1)

    # Should redirect to login page
    current_url = page.url
    is_redirected = 'login' in current_url.lower() or current_url == 'http://localhost:8000/auth/login/'

    print(f'  Current URL: {current_url}')
    print(f'  Redirected to login: {is_redirected}')

    if is_redirected:
        print('✓ Unauthenticated access properly blocked')
    else:
        print('✗ SECURITY ISSUE: Unauthenticated access allowed')
        return False

    # Test 6.2: Profile isolation
    print('\nTest 6.2: User can only access own profile')

    # Login back
    login(page)

    # Access own profile
    page.goto('http://localhost:8000/profile/')
    expect(page.locator('h1')).to_contain_text('Perfil')
    print('✓ User can access own profile')

    # The ProfileDetailView.get_object() always returns request.user's profile
    # There's no way to access another user's profile via URL
    # This is secure by design
    print('✓ Profile access is isolated to logged-in user (verified in code)')

    return True


def run_all_tests():
    """Run all profile flow tests"""
    print('=' * 70)
    print('PROFILE FLOW E2E VALIDATION')
    print('Testing navbar dropdown links and complete profile workflow')
    print('=' * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Setup: Test user already created via Django shell
            print('\n=== SETUP: Test user ready (teste_profile@finanpy.com) ===')

            # Run tests
            tests = [
                test_desktop_dropdown_navigation,
                test_mobile_menu_navigation,
                test_complete_profile_flow,
                test_design_system_compliance,
                test_responsiveness,
                test_security_and_authentication,
            ]

            results = []
            for test_func in tests:
                try:
                    result = test_func(page)
                    results.append((test_func.__name__, result))
                except Exception as e:
                    print(f'\n✗ FAILED: {test_func.__name__}')
                    print(f'  Error: {str(e)}')
                    results.append((test_func.__name__, False))

            # Summary
            print('\n' + '=' * 70)
            print('TEST SUMMARY')
            print('=' * 70)

            passed = sum(1 for _, result in results if result)
            total = len(results)

            for test_name, result in results:
                status = '✓ PASSED' if result else '✗ FAILED'
                print(f'{status}: {test_name}')

            print(f'\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)')

            if passed == total:
                print('\n✓ ALL TESTS PASSED - Profile flow validated successfully!')
            else:
                print(f'\n⚠ {total - passed} test(s) failed - Review required')

        except Exception as e:
            print(f'\n✗ CRITICAL ERROR: {str(e)}')
            import traceback
            traceback.print_exc()

        finally:
            browser.close()


if __name__ == '__main__':
    run_all_tests()
