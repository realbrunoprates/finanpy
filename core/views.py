# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

# Local imports
from accounts.models import Account
from categories.models import Category
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
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

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
        })

        return context
