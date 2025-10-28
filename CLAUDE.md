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
| transactions | Transaction | Financial transactions | models.py, views.py, forms.py |
| core | - | Settings, main URLs | settings.py, urls.py |

### Key Architectural Principles

1. **Data Isolation**: Every user-owned resource (Account, Category, Transaction) filters by `user=request.user`. Users never access other users' data.

2. **Model Relationships**:
   - User (1:1) → Profile
   - User (1:N) → Account, Category
   - Account (1:N) → Transaction
   - Category (1:N) → Transaction

3. **Balance Calculation**: Transaction create/update/delete must update the related Account balance. This is critical for data consistency.

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

### Django Shell

```bash
# Interactive Python shell with Django context
python manage.py shell
```

### Code Quality

```bash
# Check for issues (always run before committing)
python manage.py check
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
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# 3. Third-party (when added)

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

The project uses `python-decouple` for environment variable management.

**Required environment variables** (`.env` file):
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
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

```
Django==5.2.7
django-tailwind==3.8.0
python-decouple==3.8
```

**NOTE**: The project uses `django-tailwind` package which integrates TailwindCSS with Django. This requires Node.js to be installed.

## Critical Development Notes

1. **Balance Consistency**: When creating/updating/deleting transactions, ALWAYS update the related account balance. The project uses Django signals (`post_save`, `post_delete`) in `transactions/signals.py` to automatically update account balances when transactions are modified. Never update balances manually in views.

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

6. **Custom User Model**: Always use `get_user_model()` - the project uses `users.CustomUser`, not Django's default User model. The AUTH_USER_MODEL setting is configured in `core/settings.py`.

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
