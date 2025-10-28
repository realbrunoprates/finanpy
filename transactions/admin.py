from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface para o modelo Transaction.

    Permite gerenciar transações via Django Admin com filtros e busca.
    Os signals de atualização de saldo funcionam automaticamente aqui.
    """

    list_display = [
        'transaction_date',
        'account',
        'category',
        'transaction_type',
        'amount',
        'description_short',
        'created_at'
    ]

    list_filter = [
        'transaction_type',
        'transaction_date',
        'created_at',
        'account',
        'category'
    ]

    search_fields = [
        'description',
        'account__name',
        'category__name'
    ]

    date_hierarchy = 'transaction_date'

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informações Principais', {
            'fields': ('account', 'category', 'transaction_type')
        }),
        ('Valores', {
            'fields': ('amount', 'transaction_date')
        }),
        ('Descrição', {
            'fields': ('description',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def description_short(self, obj):
        """Retorna descrição truncada para list_display."""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'

    description_short.short_description = 'Descrição'

    def get_queryset(self, request):
        """
        Filtra transações por usuário se não for superuser.

        Superusers veem todas as transações.
        Usuários normais veem apenas suas transações.
        """
        qs = super().get_queryset(request)

        # Otimiza queries com select_related
        qs = qs.select_related('account', 'category', 'account__user')

        if request.user.is_superuser:
            return qs

        # Filtra por transações das contas do usuário
        return qs.filter(account__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra choices de ForeignKeys por usuário.

        Garante que usuários só vejam suas próprias contas e categorias.
        """
        if db_field.name == 'account':
            if not request.user.is_superuser:
                kwargs['queryset'] = db_field.related_model.objects.filter(
                    user=request.user
                )

        if db_field.name == 'category':
            if not request.user.is_superuser:
                kwargs['queryset'] = db_field.related_model.objects.filter(
                    user=request.user
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
