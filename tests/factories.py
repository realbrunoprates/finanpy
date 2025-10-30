"""Factory Boy definitions shared across Finanpy tests."""

from decimal import Decimal

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory

from accounts.models import Account
from categories.models import Category
from profiles.models import Profile
from transactions.models import Transaction


class UserFactory(DjangoModelFactory):
    """Factory for the custom user model."""

    email = factory.Sequence(lambda index: f'user{index}@finanpy.test')
    username = factory.LazyAttribute(lambda obj: obj.email)
    password = factory.PostGenerationMethodCall(
        'set_password',
        'TestPass123!'
    )

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)


class ProfileFactory(DjangoModelFactory):
    """Factory for user profiles."""

    user = factory.SubFactory(UserFactory)
    full_name = factory.Faker('name')
    phone = factory.Faker('phone_number')

    class Meta:
        model = Profile


class AccountFactory(DjangoModelFactory):
    """Factory for financial accounts."""

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda index: f'Account {index}')
    bank_name = factory.Faker('company')
    account_type = Account.CHECKING
    balance = Decimal('1000.00')

    class Meta:
        model = Account


class CategoryFactory(DjangoModelFactory):
    """Factory for transaction categories."""

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda index: f'Category {index}')
    category_type = Category.EXPENSE
    color = '#667eea'

    class Meta:
        model = Category


class TransactionFactory(DjangoModelFactory):
    """Factory for financial transactions."""

    account = factory.SubFactory(AccountFactory)
    transaction_type = Transaction.EXPENSE
    category = factory.SubFactory(
        CategoryFactory,
        user=factory.SelfAttribute('..account.user')
    )
    amount = Decimal('100.00')
    transaction_date = factory.LazyFunction(timezone.localdate)
    description = factory.Faker('sentence', nb_words=6)

    class Meta:
        model = Transaction
