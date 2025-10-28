# Django imports
from django import forms
from django.core.exceptions import ValidationError

# Local imports
from transactions.models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionForm(forms.ModelForm):
    """
    Formulário para criar e editar transações financeiras.
    Filtra contas e categorias do usuário logado e valida correspondência de tipos.
    """

    class Meta:
        model = Transaction
        fields = ['account', 'category', 'transaction_type', 'amount', 'transaction_date', 'description']
        labels = {
            'account': 'Conta',
            'category': 'Categoria',
            'transaction_type': 'Tipo',
            'amount': 'Valor',
            'transaction_date': 'Data',
            'description': 'Descrição',
        }
        widgets = {
            'account': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: 150.00',
                'step': '0.01',
            }),
            'transaction_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Adicione uma descrição para esta transação (opcional)',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Inicializa o formulário e filtra contas e categorias do usuário.

        Args:
            user: Usuário logado (obrigatório via kwargs)
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filtra apenas contas do usuário logado
            self.fields['account'].queryset = Account.objects.filter(user=user, is_active=True)

            # Filtra apenas categorias do usuário logado
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_amount(self):
        """
        Valida se o valor da transação é positivo.

        Returns:
            Decimal: Valor validado

        Raises:
            ValidationError: Se o valor for negativo ou zero
        """
        amount = self.cleaned_data.get('amount')

        if amount is not None and amount <= 0:
            raise ValidationError('O valor da transação deve ser maior que zero.')

        return amount

    def clean(self):
        """
        Valida se o tipo de categoria corresponde ao tipo de transação.

        Returns:
            dict: Dados limpos validados

        Raises:
            ValidationError: Se o tipo de categoria não corresponder ao tipo de transação
        """
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')

        if transaction_type and category:
            # Verifica se o tipo de categoria corresponde ao tipo de transação
            if transaction_type == Transaction.INCOME and category.category_type != Category.INCOME:
                raise ValidationError(
                    'Para transações de entrada, você deve selecionar uma categoria do tipo Receita.'
                )

            if transaction_type == Transaction.EXPENSE and category.category_type != Category.EXPENSE:
                raise ValidationError(
                    'Para transações de saída, você deve selecionar uma categoria do tipo Despesa.'
                )

        return cleaned_data
