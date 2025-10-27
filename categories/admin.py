from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_email', 'category_type', 'color', 'created_at']
    list_filter = ['category_type', 'created_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

    def user_email(self, obj):
        """Display user's email instead of user object."""
        return obj.user.email
    user_email.short_description = 'Email do Usuário'
