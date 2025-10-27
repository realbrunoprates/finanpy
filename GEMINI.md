# Gemini Context: Finanpy Project

This document provides a comprehensive overview of the Finanpy project to guide AI-driven development.

## 1. Project Overview

**Finanpy** is a web application for personal finance management built with Django. It allows users to manage bank accounts, categorize transactions, and track their financial health through a dashboard.

### Core Technologies:

*   **Backend**: Python 3.13+, Django 5.2.7
*   **Frontend**: Django Template Language, TailwindCSS
*   **Database**: SQLite3 (for development)
*   **Configuration**: Environment variables managed with `python-decouple`.
*   **Styling**: `django-tailwind` integrates TailwindCSS, configured with a custom dark theme (`theme/static_src/tailwind.config.js`).

### Architecture:

The project follows a standard Django architecture, organized into modular applications:

*   `core`: Main project configuration (`settings.py`, `urls.py`).
*   `users`: Handles user authentication and the custom user model (`CustomUser`).
*   `accounts`: Manages user bank accounts (e.g., checking, savings).
*   `categories`: Manages user-defined categories for income and expenses.
*   `transactions`: Manages individual financial transactions.
*   `profiles`: Manages user profile data.
*   `theme`: Django app designated to manage TailwindCSS assets.
*   `templates`: Contains the global HTML templates, including the `base.html` layout.

## 2. Building and Running

Follow these steps to run the project in a development environment.

### Prerequisites:

*   Python 3.13+
*   Node.js and npm (for TailwindCSS)

### Setup:

1.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install frontend dependencies:**
    ```bash
    python manage.py tailwind install
    ```
3.  **Configure environment:**
    *   Copy `.env.example` to `.env`.
    *   Set the `SECRET_KEY` in the `.env` file.
4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

### Running the Development Servers:

The project requires two processes to run concurrently.

1.  **Start the Django web server:**
    ```bash
    python manage.py runserver
    ```
2.  **Start the TailwindCSS watcher:** (in a separate terminal)
    ```bash
    python manage.py tailwind start
    ```

The application will be available at `http://127.0.0.1:8000/`.

### Testing:

```bash
# TODO: Add test execution command once test runner is configured.
# Example: python manage.py test
```

## 3. Development Conventions

Adherence to these conventions is crucial for maintaining code quality and consistency.

### General Rules:

*   **Language**:
    *   All backend and frontend code (variable names, functions, classes, comments) must be in **English**.
    *   All user-facing text (UI messages, validation errors) must be in **Portuguese**.
*   **Quotes**: **Always use single quotes (`'`)** for strings in both Python and JavaScript, unless a string contains a single quote.
*   **Style Guide**: All Python code must strictly follow the **PEP 8** style guide.

### Python/Django Specifics:

*   **Naming**:
    *   `snake_case` for variables and functions (e.g., `total_balance`).
    *   `PascalCase` for classes (e.g., `AccountView`).
*   **Models**:
    *   Every model must include `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)`.
    *   Every model must have a descriptive `__str__` method.
    *   All `ForeignKey` and `ManyToManyField` fields must define a `related_name`.
*   **Views**: Use Function-Based Views for simple logic and Class-Based Views for more complex, reusable logic.
*   **Permissions**: Always validate that `request.user` has permission to access or modify objects.

### Git Workflow:

*   **Branching**:
    *   `feature/<feature-name>`
    *   `fix/<bug-name>`
*   **Commit Messages**:
    *   Write messages in **Portuguese**.
    *   Use the **infinitive form** for verbs (e.g., "Adicionar modelo de Categoria" instead of "Adicionado modelo...").

This context provides a solid foundation for any development task. Always refer back to the `docs/` directory for more detailed information.
