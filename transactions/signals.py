# Django imports
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

# Local imports
from .models import Transaction


@receiver(pre_save, sender=Transaction)
def store_old_transaction_data(sender, instance, **kwargs):
    """
    Armazena dados da transação antes de salvar para detectar mudanças.

    Este signal é executado ANTES do save() e armazena o estado anterior
    da transação para que possamos reverter o saldo corretamente no post_save.
    """
    if instance.pk:  # Apenas para updates (não para creates)
        try:
            # Busca a versão antiga da transação do banco de dados
            old_transaction = Transaction.objects.get(pk=instance.pk)

            # Armazena dados antigos como atributos temporários na instância
            instance._old_account = old_transaction.account
            instance._old_amount = old_transaction.amount
            instance._old_transaction_type = old_transaction.transaction_type
        except Transaction.DoesNotExist:
            # Transação não existe no banco (edge case improvável)
            instance._old_account = None
            instance._old_amount = None
            instance._old_transaction_type = None


@receiver(post_save, sender=Transaction)
def update_balance_on_save(sender, instance, created, **kwargs):
    """
    Atualiza o saldo da conta quando uma transação é criada ou atualizada.

    Cenários tratados:
    - CREATE: adiciona/subtrai valor do saldo da conta
    - UPDATE sem mudança de conta: reverte valor antigo e aplica novo
    - UPDATE com mudança de conta: reverte na conta antiga e aplica na nova
    - UPDATE com mudança de tipo: ajusta cálculo conforme novo tipo

    Uses transaction.atomic() para garantir consistência dos dados.
    """
    try:
        with transaction.atomic():
            if created:
                # CENÁRIO 1: Nova transação criada
                _update_account_balance(
                    account=instance.account,
                    amount=instance.amount,
                    transaction_type=instance.transaction_type,
                    operation='add'
                )
            else:
                # CENÁRIO 2: Transação atualizada

                # Verifica se há dados da transação antiga armazenados
                if hasattr(instance, '_old_account') and instance._old_account:
                    old_account = instance._old_account
                    old_amount = instance._old_amount
                    old_transaction_type = instance._old_transaction_type

                    # Verifica se a conta mudou
                    if old_account.pk != instance.account.pk:
                        # CENÁRIO 2A: Conta foi alterada
                        # Reverte o saldo na conta antiga
                        _update_account_balance(
                            account=old_account,
                            amount=old_amount,
                            transaction_type=old_transaction_type,
                            operation='remove'
                        )

                        # Aplica o saldo na conta nova
                        _update_account_balance(
                            account=instance.account,
                            amount=instance.amount,
                            transaction_type=instance.transaction_type,
                            operation='add'
                        )
                    else:
                        # CENÁRIO 2B: Mesma conta; valor ou tipo atualizados
                        # Reverte o valor antigo
                        _update_account_balance(
                            account=old_account,
                            amount=old_amount,
                            transaction_type=old_transaction_type,
                            operation='remove'
                        )

                        # Aplica o novo valor
                        _update_account_balance(
                            account=instance.account,
                            amount=instance.amount,
                            transaction_type=instance.transaction_type,
                            operation='add'
                        )

                    # Limpa atributos temporários
                    delattr(instance, '_old_account')
                    delattr(instance, '_old_amount')
                    delattr(instance, '_old_transaction_type')

    except Exception as e:
        # Log do erro (em produção, usar logging adequado)
        print(f'Erro ao atualizar saldo da conta: {str(e)}')
        raise


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    """
    Reverte o saldo da conta quando uma transação é deletada.

    Remove o impacto da transação deletada do saldo da conta:
    - INCOME: subtrai o valor do saldo
    - EXPENSE: adiciona o valor de volta ao saldo

    Uses transaction.atomic() para garantir consistência dos dados.
    """
    try:
        with transaction.atomic():
            # Reverte a transação removendo seu impacto no saldo
            _update_account_balance(
                account=instance.account,
                amount=instance.amount,
                transaction_type=instance.transaction_type,
                operation='remove'
            )

    except Exception as e:
        # Log do erro (em produção, usar logging adequado)
        print(f'Erro ao reverter saldo da conta: {str(e)}')
        raise


def _update_account_balance(account, amount, transaction_type, operation):
    """
    Função auxiliar para atualizar o saldo de uma conta.

    Args:
        account: Instância do modelo Account
        amount: Valor decimal da transação
        transaction_type: 'income' ou 'expense'
        operation: 'add' (adicionar impacto) ou 'remove' (remover impacto)

    Lógica:
        - INCOME + add: saldo += valor (adiciona receita)
        - INCOME + remove: saldo -= valor (remove receita)
        - EXPENSE + add: saldo -= valor (adiciona despesa)
        - EXPENSE + remove: saldo += valor (remove despesa)
    """
    # Refresh para garantir que temos os dados mais recentes
    account.refresh_from_db()

    if operation == 'add':
        # Adicionando impacto da transação
        if transaction_type == Transaction.INCOME:
            account.balance += amount
        elif transaction_type == Transaction.EXPENSE:
            account.balance -= amount

    elif operation == 'remove':
        # Removendo impacto da transação (operação inversa)
        if transaction_type == Transaction.INCOME:
            account.balance -= amount
        elif transaction_type == Transaction.EXPENSE:
            account.balance += amount

    # Salva a conta com update_fields para evitar disparar outros signals
    account.save(update_fields=['balance', 'updated_at'])
