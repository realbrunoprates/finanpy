from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Configura a interface administrativa para contas do usuário."""

    list_display = [
        'name',
        'user_email',
        'bank_name',
        'account_type',
        'balance',
        'is_active',
        'created_at',
    ]
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['name', 'bank_name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'name', 'bank_name', 'account_type')
        }),
        ('Saldo', {
            'fields': ('balance',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        """Retorna o email do usuário da conta."""
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
    user_email.admin_order_field = 'user__email'

    def get_queryset(self, request):
        """Filtra contas por usuário se não for superuser."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
