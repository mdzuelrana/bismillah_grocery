from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'balance',
        'is_active',
        'is_staff',
    )
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'balance', 'shopping_preferences')
        }),
    )
