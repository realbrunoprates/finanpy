# Standard library
from datetime import datetime

# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

# Local imports
from .models import Transaction
from .forms import TransactionForm
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


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for new transactions.

    Features:
    - Filters accounts and categories by logged-in user
    - Validates category type matches transaction type
    - Automatically updates account balance via signals
    - Success message after creation
    - Proper error handling
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_form_kwargs(self):
        """
        Pass the logged-in user to the form for filtering accounts and categories.

        Returns:
            dict: Form kwargs with user added
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Handle successful form validation.

        Adds success message and saves the transaction.
        Account balance is updated automatically via signals.

        Args:
            form: Valid TransactionForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url
        """
        response = super().form_valid(form)

        # Get transaction type for customized message
        transaction_type = self.object.transaction_type
        type_label = 'receita' if transaction_type == Transaction.INCOME else 'despesa'

        messages.success(
            self.request,
            f'Transação de {type_label} criada com sucesso! O saldo da conta foi atualizado automaticamente.'
        )

        return response

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Adds error message to inform user about validation issues.

        Args:
            form: Invalid TransactionForm instance

        Returns:
            HttpResponse: Re-render form with errors
        """
        messages.error(
            self.request,
            'Erro ao criar transação. Por favor, verifique os campos e tente novamente.'
        )

        return super().form_invalid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update view for editing existing transactions.

    Features:
    - Filters transactions by user ownership (via account__user relationship)
    - Filters accounts and categories by logged-in user
    - Validates category type matches transaction type
    - Automatically updates account balance via signals
    - Success message after update
    - Proper error handling
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        """
        Filter transactions by user ownership.

        CRITICAL: This ensures users can only edit their own transactions
        by filtering through the account relationship.

        Returns:
            QuerySet: Transactions that belong to the logged-in user
        """
        return Transaction.objects.select_related(
            'account',
            'category'
        ).filter(
            account__user=self.request.user
        )

    def get_form_kwargs(self):
        """
        Pass the logged-in user to the form for filtering accounts and categories.

        Returns:
            dict: Form kwargs with user added
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Handle successful form validation.

        Adds success message and saves the transaction.
        Account balance is updated automatically via signals.

        Args:
            form: Valid TransactionForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url
        """
        response = super().form_valid(form)

        messages.success(
            self.request,
            'Transação atualizada com sucesso!'
        )

        return response

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Adds error message to inform user about validation issues.

        Args:
            form: Invalid TransactionForm instance

        Returns:
            HttpResponse: Re-render form with errors
        """
        messages.error(
            self.request,
            'Erro ao atualizar transação. Por favor, verifique os campos e tente novamente.'
        )

        return super().form_invalid(form)
