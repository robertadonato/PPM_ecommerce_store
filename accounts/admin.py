from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_store_manager')
    list_filter = ('is_store_manager', 'groups')
    actions = ['make_manager']

    @admin.action(description='Promuovi a Manager')
    def make_manager(self, request, queryset):
        queryset.update(is_store_manager=True)

admin.site.register(CustomUser, CustomUserAdmin)