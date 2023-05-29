from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role', 'first_name', 'last_name',
    )
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    ordering = ('username',)


admin.site.register(User, UserAdmin)
