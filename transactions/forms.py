# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import Account
from categories.models import Category
# Local imports
from transactions.models import Transaction

INPUT_STYLE_CLASSES = (
    'w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg '
    'text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 '
    'focus:border-transparent transition-all duration-200'
)


class TransactionForm(forms.ModelForm):
    """
    Formulário para criar e editar transações financeiras.
    Filtra contas/categorias do usuário e valida tipos compatíveis.
    """

    class Meta:
        """Define campos e widgets utilizados no formulário de transações."""

        model = Transaction
        fields = [
            'account',
            'category',
            'transaction_type',
            'amount',
            'transaction_date',
            'description',
        ]
        labels = {
            'account': 'Conta',
            'category': 'Categoria',
            'transaction_type': 'Tipo',
            'amount': 'Valor',
            'transaction_date': 'Data',
            'description': 'Descrição',
        }
        widgets = {
            'account': forms.Select(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                }
            ),
            'transaction_type': forms.Select(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                    'placeholder': 'Ex: 150.00',
                    'step': '0.01',
                    'min': '0.01',
                }
            ),
            'transaction_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': INPUT_STYLE_CLASSES,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': INPUT_STYLE_CLASSES,
                    'placeholder': (
                        'Adicione uma descrição para esta transação '
                        '(opcional)'
                    ),
                    'rows': 4,
                }
            ),
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
            self.fields['account'].queryset = Account.objects.filter(
                user=user,
                is_active=True,
            )

            # Filtra apenas categorias do usuário logado
            self.fields['category'].queryset = Category.objects.filter(
                user=user,
            )

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
            raise ValidationError(
                'O valor da transação deve ser maior que zero.'
            )

        return amount

    def clean_transaction_date(self):
        """
        Valida se a data da transação não está no futuro.

        Returns:
            date: Data validada da transação

        Raises:
            ValidationError: Se a data estiver no futuro
        """
        transaction_date = self.cleaned_data.get('transaction_date')

        if transaction_date and transaction_date > timezone.localdate():
            raise ValidationError(
                'A data da transação não pode estar no futuro.'
            )

        return transaction_date

    def clean(self):
        """
        Valida se o tipo de categoria corresponde ao tipo de transação
        e verifica se há saldo suficiente para transações de despesa.

        Returns:
            dict: Dados limpos validados

        Raises:
            ValidationError: Categoria não compatível com o tipo
        """
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')

        if transaction_type and category:
            # Verifica se o tipo de categoria corresponde ao tipo de transação
            if (
                transaction_type == Transaction.INCOME
                and category.category_type != Category.INCOME
            ):
                raise ValidationError(
                    (
                        'Para transações de entrada, você deve selecionar '
                        'uma categoria do tipo Receita.'
                    )
                )

            if (
                transaction_type == Transaction.EXPENSE
                and category.category_type != Category.EXPENSE
            ):
                raise ValidationError(
                    (
                        'Para transações de saída, você deve selecionar '
                        'uma categoria do tipo Despesa.'
                    )
                )

        if (
            transaction_type == Transaction.EXPENSE
            and account
            and amount is not None
        ):
            available_balance = account.balance

            if self.instance.pk:
                try:
                    old_transaction = Transaction.objects.get(
                        pk=self.instance.pk
                    )
                except Transaction.DoesNotExist:
                    old_transaction = None
                else:
                    if old_transaction.account_id == account.pk:
                        if (
                            old_transaction.transaction_type
                            == Transaction.EXPENSE
                        ):
                            available_balance += old_transaction.amount
                        elif (
                            old_transaction.transaction_type
                            == Transaction.INCOME
                        ):
                            available_balance -= old_transaction.amount

            if amount > available_balance:
                raise ValidationError(
                    {
                        'amount': (
                            'Saldo insuficiente na conta selecionada '
                            'para esta despesa.'
                        )
                    }
                )

        return cleaned_data
