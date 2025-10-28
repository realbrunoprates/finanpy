# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import redirect

# Local imports
from .models import Account
from .forms import AccountForm


class AccountListView(LoginRequiredMixin, ListView):
    """
    View for listing all accounts of the logged-in user.
    Displays account information and calculates total balance.
    """
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 9
    per_page_options = (6, 9, 12, 18)

    def get_queryset(self):
        """
        Return only accounts belonging to the logged-in user.
        Orders results by name.
        """
        return Account.objects.filter(
            user=self.request.user
        ).order_by('name')

    def get_context_data(self, **kwargs):
        """
        Add total balance and breadcrumbs to context.
        Calculates the sum of all account balances for the user.
        """
        context = super().get_context_data(**kwargs)

        # Calculate total balance from all user accounts
        total_balance = Account.objects.filter(
            user=self.request.user
        ).aggregate(
            total=Sum('balance')
        )['total'] or 0

        context['total_balance'] = total_balance
        context['per_page_options'] = self.per_page_options
        context['current_per_page'] = getattr(
            self,
            '_current_per_page',
            self.paginate_by
        )

        # Add breadcrumbs
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Contas', 'url': None}
        ]

        return context

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


class AccountCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new account.
    Automatically associates the account with the logged-in user.
    """
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:list')

    def form_valid(self, form):
        """
        Associate the logged-in user with the account before saving.
        Display success message after account creation.
        """
        # Associate account with logged-in user
        form.instance.user = self.request.user

        # Add success message
        messages.success(self.request, 'Conta criada com sucesso!')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add page title and breadcrumbs to context.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Conta'

        # Add breadcrumbs
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Contas', 'url': 'accounts:list'},
            {'label': 'Nova Conta', 'url': None}
        ]

        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing account that belongs to the logged-in user.
    """
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:list')

    def get_queryset(self):
        """
        Restrict queryset to accounts owned by the logged-in user.
        """
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Persist changes and display a success message after updating the account.
        """
        messages.success(self.request, 'Conta atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add page title and breadcrumbs to context.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Conta'

        # Add breadcrumbs
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Contas', 'url': 'accounts:list'},
            {'label': 'Editar', 'url': None}
        ]

        return context


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting an existing account that belongs to the logged-in user.
    Displays a confirmation page before deletion.
    """
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts:list')

    def get_queryset(self):
        """
        Restrict queryset to accounts owned by the logged-in user.
        """
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add breadcrumbs to context.
        """
        context = super().get_context_data(**kwargs)

        # Add breadcrumbs
        context['breadcrumbs'] = [
            {'label': 'Home', 'url': 'home'},
            {'label': 'Contas', 'url': 'accounts:list'},
            {'label': 'Excluir', 'url': None}
        ]

        return context

    def form_valid(self, form):
        """
        Validate deletion to prevent removing accounts with transactions.
        """
        account = self.object

        if account.transactions.exists():
            messages.error(
                self.request,
                'Não é possível excluir esta conta pois ela possui transações associadas.'
            )
            return redirect('accounts:list')

        messages.success(self.request, 'Conta excluída com sucesso!')
        return super().form_valid(form)
