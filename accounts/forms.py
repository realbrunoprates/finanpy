# Django
from django import forms

# Local imports
from .models import Account


class AccountForm(forms.ModelForm):
    """
    Formulário para criar e editar contas bancárias.
    """

    # Override account_type to customize choices labels
    account_type = forms.ChoiceField(
        label='Tipo de Conta',
        choices=[
            (Account.CHECKING, 'Conta Corrente'),
            (Account.SAVINGS, 'Poupança'),
            (Account.WALLET, 'Carteira'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200'
        })
    )

    class Meta:
        """Configura campos, rótulos e widgets do formulário."""

        model = Account
        fields = ['name', 'bank_name', 'account_type', 'balance']
        labels = {
            'name': 'Nome da Conta',
            'bank_name': 'Nome do Banco',
            'account_type': 'Tipo de Conta',
            'balance': 'Saldo Inicial',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Conta Corrente Principal'
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Banco do Brasil'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }

    def clean_name(self):
        """Validate that name has at least 3 characters."""
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('O nome da conta deve ter pelo menos 3 caracteres.')
        return name

    def clean_balance(self):
        """Validate that balance is not negative."""
        balance = self.cleaned_data['balance']
        if balance < 0:
            raise forms.ValidationError('O saldo inicial não pode ser negativo.')
        return balance
