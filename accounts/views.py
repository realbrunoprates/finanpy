# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Sum

# Local imports
from .models import Account


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
