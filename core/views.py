# Standard library
from datetime import timedelta

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

# Local imports
from accounts.models import Account
from transactions.models import Transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal do usuário com resumo financeiro.
    Exibe saldos, transações recentes e estatísticas do mês.
    """
    template_name = 'dashboard.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        """
        Adiciona dados financeiros do usuário ao contexto do template.
        """
        context = super().get_context_data(**kwargs)

        # Get current user
        user = self.request.user

        # Get current month start and end dates
        now = timezone.now()
        current_month_start = now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        # Calculate total balance from all user accounts
        total_balance = Account.objects.filter(
            user=user
        ).aggregate(
            total=Sum('balance')
        )['total'] or 0

        # Calculate total income for current month
        total_income_month = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.INCOME,
            transaction_date__gte=current_month_start.date()
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate total expenses for current month
        total_expenses_month = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.EXPENSE,
            transaction_date__gte=current_month_start.date()
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Calculate month balance (income - expenses)
        month_balance = total_income_month - total_expenses_month

        # Get last 10 transactions ordered by date
        recent_transactions = Transaction.objects.filter(
            account__user=user
        ).select_related(
            'account',
            'category'
        ).order_by(
            '-transaction_date',
            '-created_at'
        )[:10]

        # Calculate totals by category for current month
        # Income categories
        income_by_category = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.INCOME,
            transaction_date__gte=current_month_start.date()
        ).values(
            'category__name',
            'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Expense categories
        expenses_by_category = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.EXPENSE,
            transaction_date__gte=current_month_start.date()
        ).values(
            'category__name',
            'category__color'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Count active accounts
        active_accounts_count = Account.objects.filter(
            user=user,
            is_active=True
        ).count()

        # ========================================
        # Chart.js Data Preparation
        # ========================================

        # 1. Pie Chart: Expenses by category for current month
        # Prepare data for Chart.js pie chart (categories, values, colors)
        chart_categories_data = {
            'labels': [],
            'values': [],
            'colors': [],
        }

        for category_data in expenses_by_category:
            chart_categories_data['labels'].append(
                category_data['category__name']
            )
            chart_categories_data['values'].append(
                float(category_data['total'])
            )
            chart_categories_data['colors'].append(
                category_data['category__color']
            )

        # 2. Line Chart: Income vs Expenses for last 6 months
        # Calculate start date for 6 months ago
        six_months_ago = now - timedelta(days=180)
        first_day_six_months_ago = six_months_ago.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        # Prepare data structure for monthly evolution
        chart_monthly_data = {
            'labels': [],
            'income': [],
            'expenses': [],
        }

        # Portuguese month abbreviations mapping
        month_names_pt = {
            1: 'Jan',
            2: 'Fev',
            3: 'Mar',
            4: 'Abr',
            5: 'Mai',
            6: 'Jun',
            7: 'Jul',
            8: 'Ago',
            9: 'Set',
            10: 'Out',
            11: 'Nov',
            12: 'Dez',
        }

        # Iterate through last 6 months
        current_date = first_day_six_months_ago
        for i in range(6):
            # Calculate month boundaries
            month_start = current_date.replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(
                    year=month_start.year + 1,
                    month=1,
                    day=1,
                )
            else:
                month_end = month_start.replace(
                    month=month_start.month + 1,
                    day=1,
                )

            # Get month name in Portuguese
            month_label = month_names_pt[month_start.month]
            chart_monthly_data['labels'].append(month_label)

            # Calculate income for this month
            income_total = Transaction.objects.filter(
                account__user=user,
                transaction_type=Transaction.INCOME,
                transaction_date__gte=month_start.date(),
                transaction_date__lt=month_end.date(),
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

            # Calculate expenses for this month
            expenses_total = Transaction.objects.filter(
                account__user=user,
                transaction_type=Transaction.EXPENSE,
                transaction_date__gte=month_start.date(),
                transaction_date__lt=month_end.date(),
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

            chart_monthly_data['income'].append(float(income_total))
            chart_monthly_data['expenses'].append(float(expenses_total))

            # Move to next month
            current_date = month_end

        # Add all data to context
        context.update({
            'total_balance': total_balance,
            'total_income_month': total_income_month,
            'total_expenses_month': total_expenses_month,
            'month_balance': month_balance,
            'recent_transactions': recent_transactions,
            'income_by_category': income_by_category,
            'expenses_by_category': expenses_by_category,
            'active_accounts_count': active_accounts_count,
            'current_month': now.strftime('%B %Y'),
            'chart_categories_data': chart_categories_data,
            'chart_monthly_data': chart_monthly_data,
        })

        return context
