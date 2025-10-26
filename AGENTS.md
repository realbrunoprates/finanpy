# Repository Guidelines

## Project Structure & Module Organization
The Django project centers on `manage.py`. Configuration lives in `core/`, while domain apps sit in `accounts/`, `categories/`, `transactions/`, `profiles/`, and `users/`—each with models, forms, views, and `tests.py`. Shared templates are under `templates/`, static files in `static/`, and Tailwind assets in `theme/`. Documentation starts in `docs/`, and task briefs for automation agents are in `agents/`.

## Build, Test, and Development Commands
Activate the virtualenv (`source venv/bin/activate`) and install dependencies with `pip install -r requirements.txt`. Start the dev server via `python manage.py runserver`. Watch Tailwind with `python manage.py tailwind start`. For a production CSS bundle run `python manage.py tailwind build` followed by `python manage.py collectstatic`. Apply schema changes using `python manage.py makemigrations` then `python manage.py migrate`.

## Coding Style & Naming Conventions
Follow PEP 8, using 4-space indentation and keeping lines under 79 characters. Prefer single quotes for strings; reserve double quotes for embedded apostrophes. Keep identifiers in English (`calculate_total`), while user-facing messages stay in Portuguese (`messages.success(..., 'Conta criada!')`). Use `snake_case` for functions and variables, `PascalCase` for classes, and `UPPER_CASE` for constants. Order imports as standard library, third-party, then local modules.

## Testing Guidelines
Write Django `TestCase` classes in each app’s `tests.py`. Name classes `Test...` and methods `test_...` to describe behaviour. Run the suite with `python manage.py test`. Add regression tests with bug fixes and cover balance calculations, permission checks, and form validation logic. Prefer fixtures or factories over ad-hoc data so tests stay deterministic.

## Commit & Pull Request Guidelines
Write commit messages in Portuguese, infinitive mood (`"Corrigir cálculo de saldo"`). Name branches by scope: `feature/...`, `fix/...`, or `hotfix/...`. Before pushing, run tests and Tailwind build when styles change. Pull requests must outline the change, reference related TASKS or issues, list affected apps, and add screenshots for UI updates. Mention touched docs and keep `.env` secrets out of version control.

## Security & Configuration Tips
Keep environment secrets in `.env` and never commit the file. Disable `DEBUG` for production deployments. Validate object ownership in views, require authenticated access for dashboards, and audit new endpoints for permission checks before merging.
