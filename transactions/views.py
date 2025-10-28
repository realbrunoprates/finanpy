# Standard library
from datetime import datetime

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.views.generic import ListView

# Local imports
from .models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionListView(LoginRequiredMixin, ListView):
    """
    List view for transactions with filtering and statistics.

    Features:
    - Filter by user ownership through account relationship
    - Filter by date range (data_inicio, data_fim)
    - Filter by account (conta)
    - Filter by category (categoria)
    - Pagination (20 transactions per page)
    - Statistics: total income, total expense, balance
    """
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        """
        Filter transactions by user and apply GET parameter filters.

        Returns:
            QuerySet: Filtered and optimized transactions queryset
        """
        # Base queryset: filter by user through account relationship
        # Optimize queries with select_related to avoid N+1 queries
        queryset = Transaction.objects.select_related(
            'account',
            'category'
        ).filter(
            account__user=self.request.user
        ).order_by('-transaction_date', '-created_at')

        # Filter by date range
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if data_inicio:
            try:
                # Parse date in format YYYY-MM-DD
                data_inicio_parsed = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                queryset = queryset.filter(transaction_date__gte=data_inicio_parsed)
            except ValueError:
                # Invalid date format, ignore filter
                pass

        if data_fim:
            try:
                # Parse date in format YYYY-MM-DD
                data_fim_parsed = datetime.strptime(data_fim, '%Y-%m-%d').date()
                queryset = queryset.filter(transaction_date__lte=data_fim_parsed)
            except ValueError:
                # Invalid date format, ignore filter
                pass

        # Filter by account
        conta = self.request.GET.get('conta')
        if conta:
            try:
                conta_id = int(conta)
                queryset = queryset.filter(account_id=conta_id)
            except (ValueError, TypeError):
                # Invalid account ID, ignore filter
                pass

        # Filter by category
        categoria = self.request.GET.get('categoria')
        if categoria:
            try:
                categoria_id = int(categoria)
                queryset = queryset.filter(category_id=categoria_id)
            except (ValueError, TypeError):
                # Invalid category ID, ignore filter
                pass

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add statistics and filter options to context.

        Returns:
            dict: Context with transactions, statistics, and filter data
        """
        context = super().get_context_data(**kwargs)

        # Get filtered queryset (respects all applied filters)
        filtered_queryset = self.get_queryset()

        # Calculate statistics using aggregation
        income_aggregate = filtered_queryset.filter(
            transaction_type=Transaction.INCOME
        ).aggregate(total=Sum('amount'))

        expense_aggregate = filtered_queryset.filter(
            transaction_type=Transaction.EXPENSE
        ).aggregate(total=Sum('amount'))

        total_income = income_aggregate['total'] or 0
        total_expense = expense_aggregate['total'] or 0
        balance = total_income - total_expense

        # Add statistics to context
        context['total_income'] = total_income
        context['total_expense'] = total_expense
        context['balance'] = balance

        # Add filter options to context
        # List of user's accounts for dropdown
        context['user_accounts'] = Account.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('name')

        # List of user's categories for dropdown
        context['user_categories'] = Category.objects.filter(
            user=self.request.user
        ).order_by('name')

        # Preserve current filter values for form population
        context['filter_data_inicio'] = self.request.GET.get('data_inicio', '')
        context['filter_data_fim'] = self.request.GET.get('data_fim', '')
        context['filter_conta'] = self.request.GET.get('conta', '')
        context['filter_categoria'] = self.request.GET.get('categoria', '')

        return context
