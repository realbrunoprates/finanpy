from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'full_name', 'phone', 'created_at']
    search_fields = ['user__email', 'full_name']
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['created_at']

    def user__email(self, obj):
        return obj.user.email
    user__email.short_description = 'Email'
    user__email.admin_order_field = 'user__email'
