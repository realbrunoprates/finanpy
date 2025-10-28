# Standard library
from datetime import datetime, timedelta

# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
    - Filter by search query in description (search or q parameter)
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
    per_page_options = (10, 20, 50, 100)
    sortable_fields = {
        'date': 'transaction_date',
        'description': 'description',
        'amount': 'amount',
        'account': 'account__name',
        'category': 'category__name',
        'type': 'transaction_type',
    }
    default_sort = 'date'
    default_direction = 'desc'

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
        )

        # Filter by search query (description)
        search = self.request.GET.get('search') or self.request.GET.get('q')
        if search:
            # Case-insensitive search in description field
            queryset = queryset.filter(
                Q(description__icontains=search)
            )

        # Quick date filters have priority over manual date range
        quick_filter = self.request.GET.get('period') or self.request.GET.get('quick_filter')

        if quick_filter:
            # Store active quick filter for context
            self.active_quick_filter = quick_filter

            # Calculate date range based on quick filter
            today = datetime.now().date()
            data_inicio_parsed = None
            data_fim_parsed = None

            if quick_filter == 'this_month':
                # First day of current month to today
                data_inicio_parsed = today.replace(day=1)
                data_fim_parsed = today

            elif quick_filter == 'last_month':
                # First day of last month to last day of last month
                first_day_this_month = today.replace(day=1)
                last_day_last_month = first_day_this_month - timedelta(days=1)
                data_inicio_parsed = last_day_last_month.replace(day=1)
                data_fim_parsed = last_day_last_month

            elif quick_filter == 'this_year':
                # First day of current year to today
                data_inicio_parsed = today.replace(month=1, day=1)
                data_fim_parsed = today

            elif quick_filter == 'last_30_days':
                # 30 days ago to today
                data_inicio_parsed = today - timedelta(days=30)
                data_fim_parsed = today

            elif quick_filter == 'last_90_days':
                # 90 days ago to today
                data_inicio_parsed = today - timedelta(days=90)
                data_fim_parsed = today

            # Apply calculated date filters
            if data_inicio_parsed:
                queryset = queryset.filter(transaction_date__gte=data_inicio_parsed)
            if data_fim_parsed:
                queryset = queryset.filter(transaction_date__lte=data_fim_parsed)

        else:
            # No quick filter active
            self.active_quick_filter = None

            # Filter by manual date range (only if no quick filter)
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

        sort_key, direction, ordering = self.get_ordering_params()
        self.current_sort = sort_key
        self.current_direction = direction

        return queryset.order_by(*ordering)

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
        context['accounts'] = Account.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('name')

        # List of user's categories for dropdown
        context['categories'] = Category.objects.filter(
            user=self.request.user
        ).order_by('name')

        # Preserve current filter values for form population
        context['filter_search'] = self.request.GET.get('search') or self.request.GET.get('q', '')
        context['filter_data_inicio'] = self.request.GET.get('data_inicio', '')
        context['filter_data_fim'] = self.request.GET.get('data_fim', '')
        context['filter_conta'] = self.request.GET.get('conta', '')
        context['filter_categoria'] = self.request.GET.get('categoria', '')

        # Add active quick filter to context
        context['active_quick_filter'] = getattr(self, 'active_quick_filter', None)

        # Breadcrumbs for navigation
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Transações', 'url': None},
        ]

        context['current_sort'] = getattr(
            self,
            'current_sort',
            self.default_sort
        )
        context['current_direction'] = getattr(
            self,
            'current_direction',
            self.default_direction
        )
        context['sorting_metadata'] = self.get_sorting_metadata()
        context['per_page_options'] = self.per_page_options
        context['current_per_page'] = getattr(
            self,
            '_current_per_page',
            self.paginate_by
        )

        return context

    def get_ordering_params(self):
        """
        Resolve ordering based on `sort` and `direction` query params.
        """
        sort_param = self.request.GET.get('sort', self.default_sort)
        direction_param = self.request.GET.get(
            'direction',
            self.default_direction
        )

        is_sort_valid = sort_param in self.sortable_fields
        sort_key = (
            sort_param
            if is_sort_valid
            else self.default_sort
        )
        direction = (
            direction_param
            if direction_param in {'asc', 'desc'}
            else self.default_direction
        )

        if not is_sort_valid:
            direction = self.default_direction

        field_name = self.sortable_fields[sort_key]
        prefix = '' if direction == 'asc' else '-'
        ordering = [f'{prefix}{field_name}']

        if field_name != 'transaction_date':
            ordering.append(
                'transaction_date' if direction == 'asc' else '-transaction_date'
            )

        ordering.append(
            'created_at' if direction == 'asc' else '-created_at'
        )

        return sort_key, direction, ordering

    def get_paginate_by(self, queryset):
        """
        Allow dynamic page size via `per_page` GET parameter.
        """
        if hasattr(self, '_current_per_page'):
            return self._current_per_page

        per_page = self.request.GET.get('per_page')
        current = self.paginate_by

        if per_page:
            try:
                parsed = int(per_page)
            except (TypeError, ValueError):
                parsed = self.paginate_by
            else:
                if parsed not in self.per_page_options:
                    parsed = self.paginate_by
            current = parsed

        self._current_per_page = current
        return current

    def get_sorting_metadata(self):
        """
        Build helper metadata used to render sorting controls.
        """
        current_sort = getattr(self, 'current_sort', self.default_sort)
        current_direction = getattr(
            self,
            'current_direction',
            self.default_direction
        )

        metadata = {}

        for key in self.sortable_fields:
            is_active = key == current_sort
            next_direction = (
                'desc' if is_active and current_direction == 'asc'
                else 'asc'
            )
            metadata[key] = {
                'is_active': is_active,
                'current_direction': current_direction if is_active else None,
                'next_direction': next_direction,
            }

        return metadata


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

    def get_context_data(self, **kwargs):
        """
        Adiciona título e breadcrumbs ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Transação'
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Transações', 'url': 'transactions:list'},
            {'label': 'Nova Transação', 'url': None},
        ]
        return context


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

    def get_context_data(self, **kwargs):
        """
        Adiciona título e breadcrumbs ao contexto.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Transação'
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Transações', 'url': 'transactions:list'},
            {'label': 'Editar Transação', 'url': None},
        ]
        return context


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete view for removing existing transactions.

    Features:
    - Filters transactions by user ownership (via account__user relationship)
    - Displays confirmation page before deletion
    - Automatically updates account balance via signals after deletion
    - Success message after deletion
    - Security: Prevents users from deleting other users' transactions
    """
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        """
        Filter transactions by user ownership.

        CRITICAL: This ensures users can only delete their own transactions
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

    def delete(self, request, *args, **kwargs):
        """
        Delete the transaction and display a success message.

        The account balance is automatically updated via post_delete signal
        defined in transactions/signals.py.

        Args:
            request: HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to success_url
        """
        messages.success(self.request, 'Transação excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adiciona breadcrumbs ao contexto para navegação consistente.
        """
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Transações', 'url': 'transactions:list'},
            {'label': 'Excluir Transação', 'url': None},
        ]
        return context
