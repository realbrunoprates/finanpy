# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Finanpy is a personal finance management system built with Django 5+ and Python 3.13+. The project follows a traditional Django monolithic architecture with server-side rendering using Django Template Language and TailwindCSS for styling. The focus is on simplicity and avoiding over-engineering.

**Core Purpose**: Allow users to manage personal finances through bank accounts, categorized transactions, and a financial dashboard.

## Project Structure

The codebase is organized into 5 main Django apps with single responsibilities:

- **users/** - User authentication and management (custom User model)
- **profiles/** - User profiles with additional information (1:1 with User)
- **accounts/** - Bank accounts management (checking, savings, wallet)
- **categories/** - Transaction categories (income/expense types)
- **transactions/** - Financial transactions (linked to accounts and categories)
- **core/** - Django project settings and global configuration
- **theme/** - TailwindCSS integration app (managed by django-tailwind)

### App Responsibilities

Each app has a single, well-defined responsibility:

| App | Models | Purpose | Key Files |
|-----|--------|---------|-----------|
| users | CustomUser | Authentication, login/logout/register | views.py, forms.py |
| profiles | Profile | User profile information | models.py, views.py |
| accounts | Account | Bank account management | models.py, views.py, forms.py |
| categories | Category | Transaction categorization | models.py, views.py, forms.py |
| transactions | Transaction | Financial transactions | models.py, views.py, forms.py, signals.py |
| core | - | Settings, main URLs | settings/, urls.py |

### Key Architectural Principles

1. **Data Isolation**: Every user-owned resource (Account, Category, Transaction) filters by `user=request.user`. Users never access other users' data.

2. **Model Relationships**:
   - User (1:1) → Profile
   - User (1:N) → Account, Category
   - Account (1:N) → Transaction
   - Category (1:N) → Transaction

3. **Balance Calculation**: Transaction create/update/delete automatically updates the related Account balance via Django signals in `transactions/signals.py`. This is critical for data consistency. **NEVER manually update account balances in views** - always let the signals handle it.

4. **All models must have**: `created_at` and `updated_at` fields (auto_now_add and auto_now).

## Development Commands

### Initial Setup

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file from example (required)
cp .env.example .env
# Edit .env and set SECRET_KEY and DEBUG=True

# 4. Install TailwindCSS dependencies
python manage.py tailwind install

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser
```

### Running the Application

**You need TWO terminal windows running simultaneously:**

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: TailwindCSS watch mode (auto-compiles CSS on changes)
python manage.py tailwind start
```

**Production build:**
```bash
# Build minified CSS
python manage.py tailwind build

# Collect static files
python manage.py collectstatic
```

### Database Operations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create specific app migration
python manage.py makemigrations app_name
```

### Testing

The project uses pytest with django-pytest plugin:

```bash
# Run all tests
pytest

# Run tests for a specific app
pytest users/tests/
pytest accounts/tests/

# Run a specific test file
pytest accounts/tests/test_models.py

# Run with coverage report
pytest --cov --cov-report=term-missing

# Run specific test class or method
pytest accounts/tests/test_views.py::TestAccountListView
pytest accounts/tests/test_views.py::TestAccountListView::test_list_only_user_accounts
```

### Django Shell

```bash
# Interactive Python shell with Django context
python manage.py shell
```

### Code Quality

```bash
# Check for issues (always run before committing)
python manage.py check

# Run flake8 linter
flake8
```

## Coding Standards

### Language and Style

- **Code**: English (variables, functions, classes, comments)
- **User-facing messages**: Portuguese (form labels, error messages, success messages)
- **Quotes**: ALWAYS use single quotes (`'`) instead of double quotes (`"`)
- **Python style**: Follow PEP 8 rigorously

### Naming Conventions

```python
# Variables and functions: snake_case
user_profile = get_user_profile()
total_balance = calculate_total_balance()

# Classes: PascalCase
class UserProfile(models.Model):
    pass

# Constants: UPPER_CASE
MAX_UPLOAD_SIZE = 5242880
DEFAULT_CURRENCY = 'BRL'
```

### Django Model Requirements

Every model MUST have:

```python
class MyModel(models.Model):
    # ... fields ...

    # Required timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # When appropriate
        verbose_name = 'Nome em Português'
        verbose_name_plural = 'Nomes em Português'

    def __str__(self):
        return self.name  # Always define
```

### Foreign Key Pattern

Always define `related_name`:

```python
class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'  # Required
    )
```

### View Security Pattern

Always validate user ownership:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    # CRITICAL: Validate ownership
    if account.user != request.user:
        return HttpResponseForbidden()

    # ... continue processing
```

### Import Organization

```python
# 1. Standard library
import os
from datetime import datetime

# 2. Django
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# 3. Third-party
# (when added)

# 4. Local imports
from accounts.models import Account
from categories.models import Category
```

## Design System

### Colors (Dark Theme)

The project uses a dark theme with purple gradient accents:

- **Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)` - Primary CTAs
- **Backgrounds**: `#0f172a` (primary), `#1e293b` (cards), `#334155` (hover)
- **Text**: `#f1f5f9` (primary), `#cbd5e1` (secondary), `#64748b` (muted)
- **Success/Income**: `#10b981` (green)
- **Error/Expense**: `#ef4444` (red)

### TailwindCSS Usage

Use utility classes consistently:

```html
<!-- Button primary with gradient -->
<button class="px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg font-medium hover:from-primary-600 hover:to-accent-600 transition-all duration-200 shadow-lg hover:shadow-xl">

<!-- Input field -->
<input class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200">

<!-- Card -->
<div class="bg-bg-secondary rounded-xl p-6 shadow-lg border border-bg-tertiary">
```

## Environment Configuration

The project uses `python-decouple` for environment variable management with a split settings structure:

### Settings Structure

The project uses separate settings files for different environments:

```
core/
├── settings/
│   ├── __init__.py      # Auto-imports development or production based on ENVIRONMENT var
│   ├── base.py          # Shared settings for all environments
│   ├── development.py   # Development-specific settings (DEBUG=True, SQLite)
│   └── production.py    # Production settings (DEBUG=False, security headers)
```

The `ENVIRONMENT` variable in `.env` determines which settings file is loaded.

### Required Environment Variables

Create a `.env` file in the project root (never commit this file):

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
ENVIRONMENT=development  # or 'production'

# Security flags (set in production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

**IMPORTANT**: Never commit the `.env` file. Use `.env.example` as template.

## Database

**Current**: SQLite3 (`db.sqlite3`)
**Future**: PostgreSQL planned for production

SQLite limitations to be aware of:
- Not ideal for concurrent writes
- Limited scalability
- Migration to PostgreSQL planned when needed

## Authentication

Using Django's authentication system with custom user model:
- **Custom User Model**: `users.CustomUser` (configured in `settings.AUTH_USER_MODEL = 'users.CustomUser'`)
- **IMPORTANT**: Always use `get_user_model()` to reference the User model, never import directly
- Email is used as the username field (`USERNAME_FIELD = 'email'`)
- Session-based authentication
- `@login_required` decorator for protected views
- CSRF protection enabled by default

```python
# Correct way to get User model
from django.contrib.auth import get_user_model

User = get_user_model()

# NEVER do this:
# from django.contrib.auth.models import User  # WRONG!
```

## Project Dependencies

### Requirements Structure

The project uses a split requirements structure:

```
requirements/
├── base.txt          # Core dependencies for all environments
├── development.txt   # Development tools (includes base.txt)
└── production.txt    # Production dependencies (includes base.txt)
```

**Main dependencies:**
```
Django==5.2.7
django-tailwind==3.8.0
python-decouple==3.8
```

**Development dependencies:**
```
pytest==8.4.2
pytest-django==4.11.1
pytest-cov==7.0.0
factory-boy==3.3.3
```

**NOTE**: The project uses `django-tailwind` package which integrates TailwindCSS with Django. This requires Node.js to be installed.

## Critical Development Notes

1. **Balance Consistency**: Transaction create/update/delete automatically updates the related Account balance via Django signals in `transactions/signals.py`. The signals handle:
   - **CREATE**: Adds (INCOME) or subtracts (EXPENSE) from account balance
   - **UPDATE**: Reverts old balance impact and applies new one (handles account changes)
   - **DELETE**: Reverts the transaction's balance impact

   **NEVER manually update account balances in views.** Always trust the signals. The logic uses `transaction.atomic()` for consistency and handles edge cases like account changes.

2. **Data Isolation**: Every query for user-owned data MUST filter by the logged-in user. Never trust URL parameters for user identification.
   ```python
   # ALWAYS do this:
   accounts = Account.objects.filter(user=request.user)

   # NEVER do this:
   accounts = Account.objects.all()  # Exposes all users' data!
   ```

3. **Template Location**: Templates go in `app_name/templates/app_name/` following Django conventions. Global templates go in `templates/` at project root.

4. **Static Files & TailwindCSS**:
   - Global static files: `static/` directory
   - TailwindCSS compiled output: `theme/static/css/dist/`
   - **IMPORTANT**: During development, you MUST run `python manage.py tailwind start` in a separate terminal alongside `python manage.py runserver`. The Tailwind watcher auto-compiles CSS on file changes.
   - Production: Run `python manage.py tailwind build` before `collectstatic`

5. **Git Commits**: Use Portuguese, infinitive verbs (e.g., "Adicionar modelo Account", "Corrigir cálculo de saldo")

6. **Custom User Model**: Always use `get_user_model()` - the project uses `users.CustomUser`, not Django's default User model. The AUTH_USER_MODEL setting is configured in `core/settings/base.py`.

7. **Signals**: The project uses Django signals for:
   - Auto-creating Profile when User is created (`profiles/signals.py`)
   - Auto-creating default Categories for new users (`categories/signals.py`)
   - Auto-updating Account balances when Transactions change (`transactions/signals.py`)

## Specialized Agent Prompts

The `agents/` directory contains specialized AI agent prompts for different development tasks:

- **`agents/backend-developer.md`** - Backend development (Django models, views, business logic)
- **`agents/frontend-developer.md`** - Frontend development (Django templates, TailwindCSS, UI components)
- **`agents/qa-tester.md`** - Testing and validation (E2E tests, design validation, bug detection)
- **`agents/tech-lead.md`** - Code review, architecture decisions, refactoring

These agents have deep knowledge of the project documentation and follow all coding standards. They can be used with Claude Code or other AI assistants by using the Task tool with the appropriate subagent_type:
- `django-backend-dev` for backend tasks
- `finanpy-frontend-dev` for frontend tasks
- `finanpy-qa-tester` for testing and validation

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- `docs/README.md` - Documentation index
- `docs/setup.md` - Installation and setup guide
- `docs/project-structure.md` - Apps and directory organization
- `docs/coding-standards.md` - Detailed coding conventions
- `docs/architecture.md` - Technical architecture and decisions
- `docs/design-system.md` - Complete UI component library with examples

Refer to `PRD.md` for complete product requirements and user stories.

## Common Development Workflows

### Adding a New Model

1. Define the model in `app_name/models.py` with required fields (`created_at`, `updated_at`, `__str__`, Meta)
2. Create and run migrations: `python manage.py makemigrations app_name && python manage.py migrate`
3. Register in admin: Update `app_name/admin.py`
4. Create forms if needed: `app_name/forms.py`
5. Add tests: `app_name/tests/test_models.py`

### Adding a New View

1. Create the view in `app_name/views.py` (use CBVs when possible)
2. Add URL pattern in `app_name/urls.py`
3. Create template in `app_name/templates/app_name/`
4. Add `@login_required` or `LoginRequiredMixin` for protected views
5. Validate user ownership for user-specific resources
6. Add tests: `app_name/tests/test_views.py`

### Modifying Transaction Logic

**CRITICAL**: If you need to change how transactions affect account balances:

1. **ONLY modify** `transactions/signals.py` - never add balance logic in views
2. The signals use `transaction.atomic()` for consistency
3. Always test balance updates with: create, update (same account), update (different account), delete
4. Run the test suite: `pytest transactions/tests/test_models.py -v`

### Before Committing

1. Run tests: `pytest`
2. Check code quality: `python manage.py check`
3. Run linter: `flake8` (if configured)
4. Ensure TailwindCSS is built: `python manage.py tailwind build` (for production)
5. Write commit message in Portuguese using infinitive verbs
