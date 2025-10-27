# Django imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum

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
        Add total balance to context.
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

        return context


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
        Add page title to context.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Conta'
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
        Add page title to context.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Conta'
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

    def delete(self, request, *args, **kwargs):
        """
        Delete the account and display a success message.
        """
        # TODO: Add validation to prevent deletion of accounts with transactions
        messages.success(self.request, 'Conta excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
